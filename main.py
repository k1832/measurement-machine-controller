# -*- coding: utf-8 -*-
from modules.visaresource import VisaResource
from modules.fg import FG
from modules.oscillo import Oscillo

"""
サンプルプログラム
"""
if __name__ == '__main__':
    # visa_path で VISA ライブラリのパスを指定
    vr = VisaResource(visa_path="C:\\Windows\\system32\\visa64.dll")

    # PCに繋がっているリソース（オシロとか）が表示される
    print(vr.print_connected_resources())

    # 上記で確認したリソースのアドレスを指定してオシロや FG を操作するためのインスタンスを生成
    oscillo_addr = 'USB0::0x????::0x????::MY????????::INSTR'
    fg_addr = 'USB0::0x????::0x????::???????::INSTR'
    oscillo: Oscillo = Oscillo(oscillo_addr)
    fg: FG = FG(fg_addr)

    # オシロの設定

    # オシロからデータの取得
    # 平均化した波形を取得するように設定されています。詳しくはは実装を見てみてください。
    # ここでは、100回で平均化した、 "MATH1" チャンネルのデータを取得しています。
    values = oscillo.get_value_list(average_count=100, target_channel="MATH1")

    # オシロのトリガーの変更
    # ここでは、チャンネル2の立ち下がり信号に対して、0.9V を閾値としてトリガーを設定しています。
    oscillo.set_trigger(ch=2, slope_positive=False, level=0.5, level="+900.50E-03")


    # FGの設定

    # FGの出力の変更
    # ch1 を交流信号（デフォルトでは矩形波）に設定
    fg.ac(ch=1)
    # ch1 の信号の周波数を 0.1MHz に設定
    fg.change_freq(ch=1, freq=0.1)
    # ch2 を直流で HIGH に設定（HIGHの電圧はインスタンス変数にベタ書きされています）
    fg.dc(ch=2, high=True)
