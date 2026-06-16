import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),  # 上矢印キー
    pg.K_DOWN: (0, +5),  # 下矢印キー
    pg.K_LEFT: (-5, 0),  # 左矢印キー
    pg.K_RIGHT: (+5, 0),  # 右矢印キー
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def gameover(screen: pg.Surface) -> None:
    ll_rct = pg.Surface((WIDTH, HEIGHT))
    ll_rct.fill((0, 0, 0))
    ll_rct.set_alpha(100)

    font = pg.font.Font(None, 80)
    txt_surf = font.render("Game Over", True, (255, 255, 255))
    txt_rct = txt_surf.get_rect()
    txt_rct.center = WIDTH // 2, HEIGHT // 2

    kk_img = pg.image.load("fig/8.png")

    kk_rct1 = kk_img.get_rect()
    kk_rct1.center = (WIDTH // 2 - 200, HEIGHT // 2)
    kk_rct2 = kk_img.get_rect()
    kk_rct2.center = (WIDTH // 2 + 200, HEIGHT // 2)

    screen.blit(ll_rct, [0, 0])
    screen.blit(txt_surf, txt_rct)
    screen.blit(kk_img, kk_rct1)
    screen.blit(kk_img, kk_rct2)
    
    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)] 

    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))
        bb_img.set_colorkey((0, 0, 0))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_imgs.append(bb_img)

    return bb_imgs, bb_accs


def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    kk_imgs = pg.image.load("ex2/fig/3.png")
    kk_dict = {
        ( 0, 0): pg.transform.rotozoom(),# キー押下がない場合
        (+5, 0): pg.transform.flip(kk_imgs, True, False), # 右
        (+5,-5): pg.transform.rotozoom(kk_imgs, 10, 1.0), # 右上
        ( 0,-5): pg.transform.rotozoom(kk_imgs, 45, 1.0) ,# 上 
    }
    return kk_dict


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect or 爆弾Rect
    戻り値：判定結果タプル（横方向判定結果，縦方向判定結果）
    True：画面内/False：画面外
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向判定
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    
    # こうかとんの初期化
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_imgs, bb_accs = init_bb_imgs()
    kk_img = kk_imgs[tuple(sum_mv)]

    # 最初（インデックス0）の爆弾でRectを作る
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)  # 横初期座標
    bb_rct.centery = random.randint(0, HEIGHT)  # 縦初期座標
    
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾Rectが重なったら
            gameover(screen)
            return
        
        screen.blit(bg_img, [0, 0]) 

        # こうかとんの移動処理
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy * bb_accs[min(tmr // 500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]

        orig_center = bb_rct.center
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height
        bb_rct.center = orig_center

        bb_rct.move_ip(avx, avy)
        
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出ていたら元の向き(vx)を反転
            vx *= -1
        if not tate:  # 縦方向にはみ出ていたら元の向き(vy)を反転
            vy *= -1
            
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()