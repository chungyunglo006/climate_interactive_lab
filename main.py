"""
Climate Interactive Laboratory Launcher.
Allows launching the complete suite or any independent experiment website directly.
"""

import sys
import os
import subprocess
import argparse

PAGES_MAP = {
    "1": "pages/1_🌍_0D_能量平衡模型.py",
    "2": "pages/2_🌐_1D_緯度能量平衡模型.py",
    "3": "pages/3_🌼_0D_經典雛菊世界.py",
    "4": "pages/4_⚪_0D_灰雛菊世界.py",
    "5": "pages/5_🌸_1D_緯度經典雛菊世界.py",
    "6": "pages/6_🌿_1D_緯度灰雛菊世界.py",
    "7": "pages/7_🗺️_2D_氣候與雛菊世界模型.py",
    "8": "pages/8_🎬_動畫與圖表匯出工坊.py",
}


def main():
    parser = argparse.ArgumentParser(
        description="氣候與生態模擬互動實驗室 (Climate & Eco Interactive Lab)"
    )
    parser.add_argument(
        "--page", "-p",
        choices=["all", "1", "2", "3", "4", "5", "6", "7", "8"],
        default="all",
        help="指定直接啟動的獨立實驗網站編號 (1~8)，或輸入 'all' 啟動綜合大廳 (預設: all)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8501,
        help="指定 Web 伺服器連接埠 (預設: 8501)"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="執行科學模型單元驗證測試"
    )

    args = parser.parse_args()

    if args.test:
        print("執行模型物理驗證測試...")
        import test_models
        return

    script_to_run = "app.py" if args.page == "all" else PAGES_MAP.get(args.page, "app.py")

    target_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_to_run)
    print("=" * 70)
    print("🌍 氣候與生態模擬互動實驗室 (Climate & Eco Sim Lab)")
    print(f"🚀 啟動目標: {os.path.basename(target_file)}")
    print(f"📡 預計連接埠: http://localhost:{args.port}")
    print("=" * 70)

    cmd = [
        sys.executable, "-m", "streamlit", "run",
        target_file,
        "--server.port", str(args.port),
        "--server.headless", "true"
    ]

    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n實驗室 Web 伺服器已安全停止。")


if __name__ == "__main__":
    main()
