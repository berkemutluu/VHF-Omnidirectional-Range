import cv2
import numpy as np
import math

# Ekran boyutları
WIDTH, HEIGHT = 800, 600
CENTER = (WIDTH // 2, HEIGHT // 3)

def draw_sine_wave(img, offset_angle, color, y_pos, label):
    """Sinüs dalgasını ve etiketi çizen yardımcı fonksiyon."""
    points = []
    for x in range(50, 750):
        # x eksenini zamana ve açıya bağlıyoruz
        angle = (x * 0.1) + (offset_angle * math.pi / 180)
        y = int(y_pos + math.sin(angle) * 30)
        points.append((x, y))
    
    cv2.polylines(img, [np.array(points)], False, color, 2)
    cv2.putText(img, label, (50, y_pos - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)

def main():
    cv2.namedWindow("VOR Phase Simulation")
    
    # Fare konumunu takip etmek için değişken
    mouse_pos = [0, 0]

    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEMOVE:
            mouse_pos[0], mouse_pos[1] = x, y

    cv2.setMouseCallback("VOR Phase Simulation", mouse_callback)

    time_step = 0
    while True:
        # Siyah arka plan oluştur
        frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

        # 1. İstasyon ve Uçak (Fare) arasındaki açıyı hesapla
        dx = mouse_pos[0] - CENTER[0]
        dy = mouse_pos[1] - CENTER[1]
        
        # Radyal açısını hesapla (Havacılıkta 0 Kuzeydir, bu yüzden koordinatları çeviriyoruz)
        # atan2(x, -y) kullanarak pusula yönüne (0-360) çeviriyoruz
        angle_rad = math.atan2(dx, -dy)
        angle_deg = (math.degrees(angle_rad) + 360) % 360

        # 2. Görsel elemanları çiz
        cv2.circle(frame, CENTER, 10, (0, 0, 255), -1) # VOR İstasyonu
        cv2.line(frame, CENTER, (mouse_pos[0], mouse_pos[1]), (100, 100, 100), 1) # Rota hattı
        cv2.circle(frame, (mouse_pos[0], mouse_pos[1]), 7, (0, 255, 0), -1) # Uçak

        # Bilgi metni
        cv2.putText(frame, f"Ucak Radyali: {int(angle_deg)} deg", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # 3. Sinüs Dalgalarını Çiz (Alt Panel)
        time_step -= 0.2 # Dalgaların akması için zaman simülasyonu
        
        # Referans Sinyali (Kuzey - Her zaman sabit)
        draw_sine_wave(frame, time_step, (255, 255, 0), 450, "Referans Sinyali (Sabit)")
        
        # Değişken Sinyal (Uçağın bulunduğu açı kadar kaymış)
        draw_sine_wave(frame, time_step - angle_deg, (0, 255, 255), 550, f"Degisken Sinyal (Faz Kaymasi: {int(angle_deg)})")

        # Görüntüle
        cv2.imshow("VOR Phase Simulation", frame)

        # 'q' tuşu ile çıkış
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()