from app import app
#import models when created
from models import db, Character, Move, Video, UserCharacter, TrainingNote, Matchup, Combo, User
import pickle
import os
import ipdb
import json
from YouTubeAPI import fetch_videos

#write object creation for fighters, moves, etc

def load_characters():
    directory = 'JSON files'

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename)) as file:
                data =  json.load(file)
                character_list = data['characters']
                for character_data in character_list:
                    character_name = character_data['name']
                    character_head_img = character_data['head_img']
                    character_main_img = character_data['main_img']
                    character_bio = character_data['bio']
                    
                    character = Character(
                        name = character_name,
                        head_img = character_head_img,
                        main_img = character_main_img,
                        bio = character_bio
                    )

                    db.session.add(character)

    db.session.commit()

def load_moves():
    directory = 'JSON files'

    for filename in os.listdir(directory):
        if filename.endswith('json'):
            with open(os.path.join(directory, filename)) as file:
                data = json.load(file)
                move_list = data['moves']
                for move_data in move_list:
                    move_name = move_data['name']
                    move_command = move_data['command']
                    move_character = move_data.get('character_id', None)
                
                    move = Move(
                        name = move_name,
                        command = move_command,
                        character_id = move_character
                    )

                    db.session.add(move)

    db.session.commit()

def load_combos():
    directory = 'JSON files'

    for filename in os.listdir(directory):
        if filename.endswith('json'):
            with open(os.path.join(directory, filename)) as file:
                data = json.load(file)
                combo_list = data['combos']
                for combo_data in combo_list:
                    combo_name = combo_data['name']
                    combo_notation = combo_data['notation']
                    combo_character = combo_data.get('character_id', None)

                    combo = Combo(
                        name = combo_name,
                        notation = combo_notation,
                        character_id = combo_character
                    )

                    db.session.add(combo)

    db.session.commit()


def load_videos():

    default_videos = {
        'Marisa': ['E9u9TyC5TU4', 'BZoam-rO1A0', 'FWcbBdK0QDA', 'ATdH42VULf0', '7w1SCscx7j0', 'pYgsESfzeOg', '1l21G9cU7v8', 'sB757Vg7iFk', ],
        'Manon': ['5h7m5IEpDko', 'pSuXvrr2KqI', 'fvOKtYdB9KM', 'gizQxCWx4Bo', '08geJ7MQ', 'fzfmHt6TyuA', 'B6qwSC76KRs ', 'ncr1K4Lgxqw', 'zA1LdaR4Doc' ],
        'Jamie': ['B_JELPmJD6w', 'KEUj5BANBrs', 'vFz-qzKtzrM', '8zJUHahzaIM', 'NYlgeMWpnhE', 'BQ7o_mT5Bos', 'xKu4bsYF1L0', 'Tu5yI0KI78k', 'd_j6-q8cfzE'],
        'Guile': ['3_3RnvP25fA', 'iGZFz6ZbJRc', '0c6dDXdwCBA', 'Zf4imG21C0c', '4oT2MJfCbvQ', '0wq8_urrtG0', 'q13IGDgVV7g', 'sRBdeBRAcvg', 'rEMmUr5Pm14'],
        'JP': ['UGFPppRCjGc', 'RDXD2s1xryY', 'Qc2J4RLuguM', 'm01tZkFI4qA', 'H3MVs5GUO3E', 'wgj_kaaqCbU', 'XUGMZVMZYYA'],
        'Luke': ['8QtRDbIE8aM', 'aucwezgb97I', 'tsQHD8WVvx4', 'Ya34J1fKDOU', 'b3BAxnaPBQQ', 'Gn6vKwD4DPM', 'tx_skgBLk-E'],
        'Juri': ['peQvaStC7kM', 'NqPBY-dcj0o', 'zsk9lsUBpOY', 'Y4EUoamQDrA', 'fuws2ebWdAk', '72rG8zOiHCU', 'n7MlTqSxYXg'],
        'Lily': ['x2qP1sbcYe8', 'e4_Ye9OXF_k', 'mt9M1-7zC-Q', 'lyTyJygOStc', 's7-ZOtW5UtI', 'vGhSZxpdAPQ', 'kmxYSo8oaFw'],
        'Ken Masters': ['vmqsVjH4DrI', 'CQvJ2yuu-dU', 'aC2e1TchO0g', 'S1RmPLOYnjA', 'ZKifiPCDPVo', 'XSiTotoje7c', 'pkUHJf_gJ9w' ],
        'E. Honda': ['bxHQ_wKhrH0', 'FDtSER6giRY', 'QlnCd_jAW4g', 'e-TM1jjNQYM', 'mugJBYerLGQ', 'MFLn3vaDd_c' ],
        'Dhalsim': ['K1Y9kKpQax0', 'VjppLRwuNVw', '9y7G7uSAAAI', 'rnlmR0w_cZA', 'VprNsoRsy8o', '1qPTqjZmjV8', 'x3Wuklyp2Ss', 'kWk7DPCyGSo'],
        'Kimberly': ['cGHHeQRhcSg', 'raIV4VAHm1Y', 'uIc8ZXv4e20', 'XSiTotoje7c', 'S3Pqe5Mk45Q', 'BG5vnBvwxb0', '-t2-IhLgZks', 'a6y4eN4otmA'],
        'Dee Jay': ['kV76g9r2jD4', 'qlznrgyQlqM', 'FWcbBdK0QDA', 'twN3VS9AEMw', 'wPl43q6FZtM', 'uhBaVMocI98', 'cp58sI-J2QY', 'H3NY05PLyio'],
        'Ryu': ['VRBV__y-h0A', '5YorOxTBOT8', '5_JhJKd1TaY', 'hQZwPTMpgB4', 'Hgq_KfLs7kU', 'a44R9JgEFUM', 'mrC1ZEifMiA'],
        'Chun-Li': ['Av7TBL1x6nA', 'mlgcxuG-190', 'pIUC6mJ_vFs', 'WboVlu7UbJs', 'uTmbt3OSk6I', 'ICq14NnSLz0', 'AAa30JycgHM', 'Ya34J1fKDOU', 'UMoQbEYHwqQ'],
        'Blanka': ['rq3w9dTUF3A', 'rvbtEi1glMU', '992mZX3V2Zs', '_SUaCa5MYXQ', '0q77LRN2lr4', '4bRw3j-2OdE'],
        'Zangief': ['NicxJ0n7kiI', 'oGyLbt5M4_I', 't2zWsJS8q9Y', 'LmW_b1KVRoY', 'tS7VrlBy86A', 'ka_khMEECOs', 'TjYNTKZPUg0'],
        'Cammy': ['zN7UaBCaT_w', 'Miag9zpaW_Q', 'RrXJIIqi1lw', 'pI5QzUWMRaY', 'e3nsNJERKMI', '0q77LRN2lr4', '4AseqmQ_8WU', 'Y91NObeTsbY']
    }

    for character_name, video_ids in default_videos.items():
        
        character = Character.query.filter_by(name=character_name).first()
        videos = fetch_videos(video_ids)

        for video_info in videos:
            video = Video(
                video_id = video_info['video_id'],
                embed_html = video_info['embed_html'],
                title = video_info['title'],
                description = video_info['description'],
                character_id = character.id
            )

            db.session.add(video)

    db.session.commit()


def clear_tables():
    # db.session.query(Character).delete()
    # db.session.query(Move).delete()
    db.session.query(Video).delete()
    db.session.query(User).delete()
    db.session.query(UserCharacter).delete()
    db.session.query(TrainingNote).delete()
    db.session.query(Matchup).delete()
    db.session.query(Combo).delete()

if __name__ == "__main__":
    with app.app_context():
        # ipdb.set_trace()
        clear_tables()
        print('Clearing tables...')
        # load_characters()
        # print('Loading characters...')
        # # load_moves()
        # print('Loading moves...')
        load_combos()
        print('Loading combos...')
        load_videos()
        print('loading videos...')
        print('Seeding complete!')
        pass