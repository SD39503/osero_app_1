document.addEventListener('DOMContentLoaded', () => {
    const boardElement = document.getElementById('board');
    const statusElement = document.getElementById('status');
    const blackCountElement = document.getElementById('black-count');
    const whiteCountElement = document.getElementById('white-count');
    const resetButton = document.getElementById('reset');

    boardElement.addEventListener('click', async (event) => {
        if (event.target.classList.contains('cell')) {
            const row = event.target.dataset.row;
            const col = event.target.dataset.col;
            const response = await fetch('/play', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ row: parseInt(row), col: parseInt(col) })
            });
            const data = await response.json();
            if (data.status === 'win') {
                alert(`${convertSymbol(data.winner)} の勝利！`);
            } else if (data.status === 'error') {
                alert(data.message);
            }
            updateBoard(data.board, data.current_player);
        }
    });

    resetButton.addEventListener('click', async () => {
        const response = await fetch('/reset', { method: 'POST' });
        const data = await response.json();
        updateBoard(data.board, data.current_player);
    });

    function updateBoard(board, currentPlayer) {
        let blackCount = 0;
        let whiteCount = 0;

        const cells = document.querySelectorAll('.cell');
        cells.forEach((cell) => {
            const row = parseInt(cell.dataset.row);
            const col = parseInt(cell.dataset.col);
            let symbol = board[row][col];

            if (symbol === 'B') {
                symbol = '●';
                blackCount++;
            } else if (symbol === 'W') {
                symbol = '○';
                whiteCount++;
            } else {
                symbol = '';
            }

            cell.textContent = symbol;
        });

        // 現在のプレイヤーとスコアを更新
        statusElement.innerHTML = `現在のプレイヤー: ${convertSymbol(currentPlayer)}`;
        blackCountElement.textContent = blackCount;
        whiteCountElement.textContent = whiteCount;
    }

    function convertSymbol(player) {
        return player === 'B' ? '●' : '○';
    }
})