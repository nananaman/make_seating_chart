import argparse
import cv2
import numpy as np
import random
import copy


def im_show(im, scale=1):
    shape = (int(im.shape[1] / scale), int(im.shape[0] / scale))
    im = cv2.resize(im, shape)
    cv2.imshow('im', im)
    cv2.waitKey()


def make_stlist(list_pass):
    stlist = []
    with open(list_pass, 'r') as f:
        for line in f:
            stlist.append(line.replace('\n', ''))
    return stlist


def make_seats(seats_pass):
    seats = []
    with open(seats_pass, 'r') as f:
        for line in f:
            l = [int(x) for x in line.split()]
            seats.append(l)
    return seats


def make_seating_chart_front(stlist, seats, shuffle=False):
    if shuffle:
        random.shuffle(stlist)
    stnum = len(stlist)
    W = 0
    for s in seats:
        if len(s) > 0:
            W += 1
    seatsnum = sum([sum(s) for s in seats])
    seatH = int(stnum / W)
    rest = stnum % W
    # print(stnum, seatsnum, W, seatH, rest)

    chart = []
    for line in seats:
        H = seatH
        if rest > 0:
            H += 1
            rest -= 1
        mem_line = []
        for block in line:
            n = block if block < H else H
            H -= n
            if len(stlist) == n:
                members = stlist
            else:
                members, stlist = stlist[:n], stlist[n:]
            mem_line.append(members)
        chart.append(mem_line)
    return chart


def make_seating_chart_center(stlist, seats, shuffle=False):
    if shuffle:
        random.shuffle(stlist)
    stnum = len(stlist)
    w = len(seats)
    seatsnum = sum([sum(s) for s in seats])

    chart = []
    for line in seats:
        mem_line = []
        for block in line:
            members = ["" for i in range(block)]
            mem_line.append(members)
        chart.append(mem_line)

    tws = [int(w / 2), int(w / 2) + 1]
    half_flag = 3
    end_flag = False
    while stnum > 0:
        for i in range(len(tws)):
            tw = tws[i]
            mem_line = []
            if len(seats[tw]) > 0:
                l = sum(seats[tw])
                if l > stnum:
                    l = stnum
                stnum -= l
                print(tw, i, len(tws), stlist)
                if stnum == 0 and len(tws) > 1 and half_flag == 3:
                    stnum = int(l / 2)
                    l = l - stnum
                    half_flag = 2
                for block in seats[tw]:
                    if not end_flag:
                        n = block if block < l else l
                        if len(stlist) == n:
                            members = stlist
                            stlist = []
                        else:
                            members, stlist = stlist[:n], stlist[n:]
                        mem_line.append(members)
                        stnum = len(stlist)
                        if half_flag == 2:
                            end_flag = True
                    else:
                        pass
                end_flag = False
            chart[tw] = mem_line
        if tws[0] > -1:
            tws[0] -= 1
        if len(tws) > 1 and tws[1] < w:
            tws[1] += 1
        if tws[0] == -1:
            tws.pop(0)
        if len(tws) > 1 and tws[1] == w:
            tws.pop(1)
        elif len(tws) > 0 and tws[0] == w:
            tws.pop(0)
        if len(tws) == 0:
            break
    return chart


def make_seat_pic(size, name, INFO, center=False):
    w = int(INFO['LINE_WIDTH']/2)
    im = np.zeros((size[0] - w * 2, size[1] - w * 2), np.uint8) + 255
    scale = int(INFO['scale'])
    fontType = cv2.FONT_HERSHEY_PLAIN
    if center:
        fh, fw = cv2.getTextSize(
            'test', scale, cv2.FONT_HERSHEY_PLAIN, cv2.LINE_AA)[0]
        height = im.shape[0]
        width = im.shape[1]
        point=(int(width/4), int(height/2))
    else:
        point=(int(10 * scale), int(20 * scale))
    cv2.putText(im, name, point, fontType, scale,
                (0, 0, 0), scale, cv2.LINE_AA)
    return im


def make_seats_pic(seats, INFO):
    w=INFO['MARGIN'] * 2
    h=INFO['MARGIN'] * 2
    for line in seats:
        h0=INFO['WAY_H']
        if len(line) > 0:
            w += INFO['SEAT_SIZE'][1]
            for s in line:
                h0 += s * INFO['SEAT_SIZE'][0]
            h0 += INFO['WAY_H']
        else:
            w += INFO['WAY_W']
        if h < h0:
            h=h0

    # 画像作成
    im=np.zeros((h, w), np.uint8) + 255

    # タイトル
    lw=INFO['LINE_WIDTH']
    lw_2=int(lw/2)
    podium=(5, 5)
    t_podium=(podium[0] + INFO['SEAT_SIZE'][1] * 2,
                podium[1] + INFO['SEAT_SIZE'][0])
    cv2.rectangle(im, podium, t_podium, (0, 0, 0,), lw)
    im_size=(INFO['SEAT_SIZE'][0], INFO['SEAT_SIZE'][1] * 2)
    im[podium[1] + lw_2:t_podium[1] - lw_2, podium[0] + lw_2:t_podium[0] -
        lw_2]=make_seat_pic(im_size, INFO['TITLE'], INFO, center=True)

    # 教卓
    lw=INFO['LINE_WIDTH']
    lw_2=int(lw/2)
    podium=(int(w/2) - INFO['SEAT_SIZE'][1], 5)
    t_podium=(podium[0] + INFO['SEAT_SIZE'][1] * 2,
                podium[1] + INFO['SEAT_SIZE'][0])
    cv2.rectangle(im, podium, t_podium, (0, 0, 0,), lw)
    im_size=(INFO['SEAT_SIZE'][0], INFO['SEAT_SIZE'][1] * 2)
    im[podium[1] + lw_2:t_podium[1] - lw_2, podium[0] + lw_2:t_podium[0] -
        lw_2]=make_seat_pic(im_size, INFO['PODIUM_NAME'], INFO, center=True)

    target=[INFO['MARGIN'], INFO['WAY_H']]
    for line in seats:
        if len(line) > 0:
            for s in line:
                for i in range(s):
                    t=copy.copy(target)
                    t[0] += INFO['SEAT_SIZE'][1]
                    t[1] += INFO['SEAT_SIZE'][0]
                    cv2.rectangle(im, tuple(target), tuple(t), (0, 0, 0), lw)
                    target[1]=t[1]
                target[1] += INFO['WAY_H']
            target[0] += INFO['SEAT_SIZE'][1]
        else:
            target[0] += INFO['WAY_W']
        target[1]=INFO['WAY_H']
    return im


def make_chart_pic(im, chart, INFO):
    target=[INFO['MARGIN'], INFO['WAY_H']]
    for line in chart:
        if len(line) > 0:
            for s in line:
                for i in range(len(s)):
                    t=copy.copy(target)
                    t[0] += INFO['SEAT_SIZE'][1]
                    t[1] += INFO['SEAT_SIZE'][0]
                    lw_2=int(INFO['LINE_WIDTH']/2)
                    im[target[1] + lw_2:t[1] - lw_2, target[0] + lw_2:t[0] - lw_2]=make_seat_pic(
                        INFO['SEAT_SIZE'], s[i], INFO)
                    target[1]=t[1]
                target[1] += INFO['WAY_H']
            target[0] += INFO['SEAT_SIZE'][1]
        else:
            target[0] += INFO['WAY_W']
        target[1]=INFO['WAY_H']
    return im


def scaling(INFO):
    scale=INFO['scale']
    INFO['SEAT_SIZE'][0]=int(INFO['SEAT_SIZE'][0] * scale)
    INFO['SEAT_SIZE'][1]=int(INFO['SEAT_SIZE'][1] * scale)
    INFO['WAY_H']=int(INFO['WAY_H'] * scale)
    INFO['WAY_W']=int(INFO['WAY_W'] * scale)
    return INFO


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('-t', '--title', required=True)
    parser.add_argument('-p', '--podium_name')
    parser.add_argument('--list_pass')
    parser.add_argument('--seats_pass')
    parser.add_argument('-o', '--out_dir')
    parser.add_argument("--sort", help="how to solve", type=str)
    args=parser.parse_args()

    list_pass=args.list_pass if args.list_pass is not None else 'list.txt'
    stlist=make_stlist(list_pass)
    podium_name=args.podium_name if args.podium_name is not None else "Teacher's Desk"
    INFO={
        'SEAT_SIZE': [30, 100],
        'WAY_H': 90,
        'WAY_W': 20,
        'MARGIN': 80,
        'LINE_WIDTH': 2,
        'DPI': 200,
        'PODIUM_NAME': podium_name,

        'TITLE': args.title,
        'A4': [8.2677, 11.6929],
        'A4_l': [11.6929, 8.2677],
        'scale': 1,
    }

    INFO['SIZE']=[int(INFO['A4'][0] * INFO['DPI']),
                    int(INFO['A4'][1] * INFO['DPI'])]
    stnum=len(stlist)
    seats_pass=args.seats_pass if args.seats_pass is not None else 'seats.txt'
    seats=make_seats(seats_pass)
    seatsnum=sum([sum(s) for s in seats])

    out_pass = args.out_dir + '/' if args.out_dir is not None else ''
    out_pass += 'seating_chart.png'

    print('Title : {0}'.format(args.title))
    print('A Number of Students : {0}'.format(stnum))
    print('A Number of Seats : {0}'.format(seatsnum))
    print('A List of Students : {0}'.format(list_pass))
    print('An Infomation of Seats : {0}'.format(seats_pass))
    print('Out : {0}'.format(out_pass))

    if args.sort == 'center':
        chart=make_seating_chart_center(stlist, seats, shuffle=True)
    else:
        chart=make_seating_chart_front(stlist, seats, shuffle=True)

    # スケーリング
    chart_im=make_seats_pic(seats, INFO)
    # print(chart_im.shape)
    sh=chart_im.shape
    long_id=0 if sh[0] > sh[1] else 1
    scale=INFO['SIZE'][long_id] / sh[long_id]
    if sh[1 - long_id] * scale > INFO['SIZE'][1 - long_id]:
        long_id=1 - long_id
        scale=INFO['SIZE'][long_id] / sh[long_id]
    INFO['scale']=scale
    # print(scale)
    INFO=scaling(INFO)

    chart_im=make_seats_pic(seats, INFO)
    chart_im=make_chart_pic(chart_im, chart, INFO)
    # print('SIZE : ({0}, {1})'.format(chart_im.shape[0], chart_im.shape[1]))
    l=int((INFO['SIZE'][0] - chart_im.shape[0]) / 2)
    t=int((INFO['SIZE'][1] - chart_im.shape[1]) / 2)
    r=l + chart_im.shape[0]
    b=t + chart_im.shape[1]
    out=np.zeros(INFO['SIZE'], np.uint8) + 255
    out[l:r, t:b]=chart_im
    im_show(out, int(INFO['scale']))
    # print(out.shape)
    cv2.imwrite(out_pass, out)


if __name__ == '__main__':
    main()
