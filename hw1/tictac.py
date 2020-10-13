'''
class for TicTac game decription and running user-computer game
'''


class TicTacGame:
    ''' class for TicTac game '''
    def __init__(self, n=3):
        self.size = n
        self.matrix = [[i + n * j + 1 for i in range(n)] for j in range(n)]
        self.vert = [0 for _ in range(n + 1)]  # last elem - main diag
        self.hor = [0 for _ in range(n + 1)]  # last elem - other diag
        self.winner = None
        self.non_empty = 0
        self.is_cross = None

    def show_board(self):
        ''' prints board representation '''
        for i in range(self.size):
            print(*self.matrix[i], sep='\t')
        print()

    def validate_input(self, readed):
        ''' returns 0 if input is nit valid and prints error message.
        if it's ok - returns int place for point '''
        readed = readed.strip()
        if readed == '0':
            if self.is_cross is None:
                self.is_cross = False
            else:
                print("Можно выбрать игру за нолики только в начале игры!!!")
                print("Для выбора ячейки введите число", end=' ')
                print(f"от 1 до {self.size ** 2}")
        elif readed.isdigit() and 1 <= int(readed) <= self.size ** 2:
            if self.is_cross is None:
                self.is_cross = True
            return int(readed)
        else:
            print(f"Ваша команда {readed} некорректна.")
            print("Можно вводить 0 в начале, чтобы играть ноликами.")
            print(f"Для выбора ячейки введите цифру от 1 до {self.size ** 2}")
        return 0

    def is_filled(self, val):
        ''' returns True if field alreasy filled '''
        return self.matrix[val // self.size][val % self.size] in ('x', '0')

    def fill_field(self, val):
        ''' fill field and recalc metrics '''
        i, j = val // self.size, val % self.size
        self.vert[i] += 1 if self.is_cross else -1
        self.hor[j] += 1 if self.is_cross else -1
        if i == j:
            self.vert[-1] += 1 if self.is_cross else -1

        if i + j == self.size - 1:
            self.hor[-1] += 1 if self.is_cross else -1

        if (abs(self.vert[i]) == self.size or abs(self.hor[j]) == self.size or
                abs(self.vert[-1]) == self.size or abs(self.hor[-1]) == self.size):
            self.winner = 'x' if self.is_cross else '0'

        self.non_empty += 1

        self.matrix[i][j] = \
            'x' if self.is_cross else '0'


    def start_game(self):
        ''' main game loop '''
        print("Привет! Первыми ходят крестики.", end=' ')
        print("Вы играете за крестики по умолчанию.")
        print("Если хотите играть ноликами - введите 0.")
        print("Введите цифру поля,", end=' ')
        print("на которое Вы хотите поставить свой крестик или нолик")

        while True:
            val = self.validate_input(input())
            if val > 0:
                val -= 1
                if self.is_filled(val):
                    print("Это место уже занято")
                    continue
                self.fill_field(val)

                checked = self.check_winner()
                if checked is not None:
                    self.print_results(checked)
                    break
                self.show_board()

                self.auto_dummy_step()
                checked = self.check_winner()
                if checked is not None:
                    self.print_results(checked)
                    break
                self.show_board()

    @staticmethod
    def print_results(checked):
        ''' prints russian text for different game results '''
        if checked == 'draw':
            print("Ничья!")
        elif checked in ('0', 'x'):
            print(f"{'Крестики' if checked == 'x' else 'Нолики'} победили!!!")

    def check_winner(self):
        ''' returns winner point or draw or None (if game isn't over) '''
        if self.winner is not None:
            return self.winner
        return 'draw' if self.non_empty == self.size ** 2 else None

    def auto_dummy_step(self):
        ''' computer algorithm for playing game '''
        for row_idx, row in enumerate(self.matrix):
            for idx, col in enumerate(row):
                if col in range(1, self.size ** 2 + 1):
                    self.matrix[row_idx][idx] = '0' if self.is_cross else 'x'
                    return


if __name__ == '__main__':
    game = TicTacGame(5)
    game.start_game()
    print("Финальная расстановка:")
    game.show_board()
