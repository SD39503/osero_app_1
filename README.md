**概要** <br>　このアプリケーションは、Flask で作成されたオセロゲームです。 <br>
プレイヤー対AI（コンピュータ）形式で、プレイヤーは黒（●）、AIは白（○）を担当します。 <br>
有効な手をクリックして相手の石をひっくり返し、最終的に多くの石を取った方が勝利となります。 <br>

**デモ動画** <br>

https://github.com/user-attachments/assets/ba29f7ca-22ac-4b76-a6f3-a0de95aa2b3f

**環境** <br>
必要条件 <br>
Python 3.8 以上 <br>

Flask インストール済み <br>

 サーバー起動 <br>
python app.py <br>
デフォルトURL: http://127.0.0.1:5000 <br>

**ルール** <br>　　
１　黒 (●) が先手で始めます。 <br>　　
２　有効なマス目をクリックして石を置きます。 なお、無粉手を選択するとポップアップで警告文がでるようになっております。 <br>
３　相手の石を挟んだら、ひっくり返して自分の石の色に変化します。 <br>　　
４　プレイヤーが手を打った後、AI (○) が自動で手を打ちます。 <br>　　
５　両プレイヤーとも手が打てない場合、ゲーム終了となります。 <br>　　

**実装予定の機能** <br>　　
現段階のAI側の手は、ルール上有効な手の中からランダムで場所を選択しています。 <br>　　
今後はAIの手を強化する方法をリサーチしていきたいと考えております。 <br>　　




