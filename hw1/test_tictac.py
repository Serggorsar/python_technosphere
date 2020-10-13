'''
testing TicTac game
'''


import io
import unittest
import unittest.mock
from tictacn import TicTacGame


class TestTicTacGame(unittest.TestCase):
    ''' class for TicTac testing '''

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_tictac_x(self, mock_stdout):
        ''' testing game in detail for x winner '''
        game = TicTacGame(2)
        game.show_board()
        self.assertIsNone(game.is_cross)
        self.assertEqual(mock_stdout.getvalue(), '1\t2\n3\t4\n\n')
        self.assertIsNone(game.check_winner())

        self.assertEqual(game.validate_input('1'), 1)
        self.assertTrue(game.is_cross)
        self.assertFalse(game.is_filled(1))
        game.fill_field(1)
        self.assertTrue(game.is_filled(1))

        game.auto_dummy_step()
        self.assertIsNone(game.check_winner())
        game.show_board()
        self.assertEqual(mock_stdout.getvalue(), '1\t2\n3\t4\n\n'+'0\tx\n3\t4\n\n')
        self.assertEqual(game.validate_input('1a'), 0)

        game.fill_field(3)
        self.assertEqual(game.check_winner(), 'x')

    def test_tictac_0(self):
        ''' testing game for 0 winner '''
        game = TicTacGame(2)
        game.fill_field(0)
        self.assertFalse(game.is_cross)

        game.auto_dummy_step()
        game.fill_field(2)
        game.auto_dummy_step()

        self.assertEqual(game.check_winner(), '0')


if __name__ == "__main__":
    unittest.main()
