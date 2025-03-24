from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# 初期化
EMPTY, BLACK, WHITE = '', 'B', 'W'
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

def initialize_board():
    """オセロ盤の初期状態"""
    board = [[EMPTY for _ in range(8)] for _ in range(8)]
    board[3][3], board[4][4] = WHITE, WHITE
    board[3][4], board[4][3] = BLACK, BLACK
    return board

# グローバル変数
board = initialize_board()
current_player = BLACK
AI_PLAYER = WHITE  # AIが担当するプレイヤー (白)

def is_valid_move(board, row, col, player):
    """有効な手かチェック"""
    if board[row][col] != EMPTY:
        return False

    opponent = BLACK if player == WHITE else WHITE
    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        found_opponent = False
        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
            r += dr
            c += dc
            found_opponent = True
        if found_opponent and 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
            return True
    return False


def apply_move(board, row, col, player):
    """石を置いて盤面を更新"""
    board[row][col] = player
    opponent = BLACK if player == WHITE else WHITE

    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        flip_positions = []
        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
            flip_positions.append((r, c))
            r += dr
            c += dc
        if flip_positions and 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
            for fr, fc in flip_positions:
                board[fr][fc] = player


def get_valid_moves(board, player):
    """プレイヤーの有効な手を取得"""
    return [(r, c) for r in range(8) for c in range(8) if is_valid_move(board, r, c, player)]


def check_winner(board):
    """勝者判定"""
    black_count = sum(row.count(BLACK) for row in board)
    white_count = sum(row.count(WHITE) for row in board)

    if black_count + white_count == 64 or (not get_valid_moves(board, BLACK) and not get_valid_moves(board, WHITE)):
        if black_count > white_count:
            return 'B'
        elif white_count > black_count:
            return 'W'
        else:
            return 'Draw'
    return None


def ai_move(board, player):
    """AIの手を選択 (ランダムな有効な手)"""
    valid_moves = get_valid_moves(board, player)
    if valid_moves:
        row, col = random.choice(valid_moves)
        apply_move(board, row, col, player)
        return row, col
    return None


def skip_turn_if_needed():
    """おける場所がない場合ターンをスキップ"""
    global current_player
    if not get_valid_moves(board, current_player):
        # ターンスキップ
        current_player = BLACK if current_player == WHITE else WHITE
        # 両方とも置けなければゲーム終了
        if not get_valid_moves(board, current_player):
            winner = check_winner(board)
            return {'status': 'win', 'winner': winner, 'board': board}
    return None


@app.route('/')
def index():
    """トップページ表示"""
    return render_template('index.html', board=board, current_player=current_player)


@app.route('/play', methods=['POST'])
def play():
    """プレイヤーの手を処理"""
    global board, current_player
    data = request.get_json()
    row, col = data['row'], data['col']

    if current_player == AI_PLAYER:
        return jsonify({'status': 'error', 'message': 'AIのターンです', 'board': board, 'current_player': current_player})

    if not is_valid_move(board, row, col, current_player):
        return jsonify({'status': 'error', 'message': '無効な手です', 'board': board, 'current_player': current_player})

    # 人間の手を適用
    apply_move(board, row, col, current_player)

    # 勝敗チェック
    winner = check_winner(board)
    if winner:
        return jsonify({'status': 'win', 'winner': winner, 'board': board})

    # プレイヤー交代
    current_player = BLACK if current_player == WHITE else WHITE

    # スキップ判定
    skip_result = skip_turn_if_needed()
    if skip_result:
        return jsonify(skip_result)

    # AIの手番なら自動的にAIがプレイ
    if current_player == AI_PLAYER:
        ai_row, ai_col = ai_move(board, AI_PLAYER)
        # AIが有効な手を置けたら交代
        if ai_row is not None:
            current_player = BLACK if current_player == WHITE else WHITE

        # スキップ判定 (AI側)
        skip_result = skip_turn_if_needed()
        if skip_result:
            return jsonify(skip_result)

        # 勝敗チェック
        winner = check_winner(board)
        if winner:
            return jsonify({'status': 'win', 'winner': winner, 'board': board})

    return jsonify({'status': 'continue', 'board': board, 'current_player': current_player})


@app.route('/reset', methods=['POST'])
def reset():
    """ゲームリセット"""
    global board, current_player
    board = initialize_board()
    current_player = BLACK
    return jsonify({'board': board, 'current_player': current_player})


if __name__ == '__main__':
    app.run(debug=True)