from .DbTestCase import DbTestCase

from pylitinhos.remote import GameManager

class TestGameManager(DbTestCase):
    USERNAME = 'fulano'
    PASSWORD = '123456'
    NICKNAME = 'fulaninho'
    ROOMNAME = 'sala X'

    def setUp(self):
        super(TestGameManager, self).setUp()

        self.game_manager = GameManager(db=self.db)

    def test_register_player_to_room(self):
        self.assertFalse(self.db.users.exist(self.USERNAME))
        user = self.given_an_existent_user()

        res = self.game_manager.room_exist(self.ROOMNAME)

        self.assertTrue(res.is_ok())
        self.assertFalse(res.bundle.get_data('exist'))

        #Criar sala com jogador
        res = self.game_manager.add_player_to_room(user.username, self.ROOMNAME)
        self.assertTrue(res.is_ok())

        player = res.bundle.get_data('player')
        self.assertIsNotNone(player)
        self.assertEqual(player.name, user.username)

    def test_get_room(self):
        room = self.given_a_room_with_some_users()
        room_name = room.name
        player_count = len(room.players)
        self.assertGreater(player_count, 1)

        self.game_manager.db = self.reset_db()
        res = self.game_manager.get_room(room_name)
        res_room = res.bundle.get_data('room')

        self.assertTrue(res.is_ok())
        self.assertIsNotNone(res_room)
        self.assertEqual(res_room.name, room_name)
        self.assertEqual(len(res_room.players), player_count)


    def given_a_room_with_some_users(self):
        u1 = self.given_an_existent_user()
        u2 = self.given_an_existent_user(username='outro usuario', nickname='nick')

        self.db.rooms.add_player(self.ROOMNAME, u1.username)
        self.db.rooms.add_player(self.ROOMNAME, u2.username)

        return self.db.rooms.get(self.ROOMNAME)

    def given_an_existent_user(self, **kw):
        return self.db.users.create(kw.get('username', self.USERNAME),
                                    kw.get('password', self.PASSWORD),
                                    nickname=kw.get('nickname', self.NICKNAME))