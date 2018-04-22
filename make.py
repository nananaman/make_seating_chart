import cv2
import numpy as np
import random
import copy


def make_title_and_stlist(list_pass):
    stlist = []
    with open(list_pass, 'r') as f:
        for line in f:
            stlist.append(line.replace('\n', ''))
    return stlist[0], stlist[1:]


def make_seats(seats_pass):
    seats = []
    with open(seats_pass, 'r') as f:
        for line in f:
            l = [int(x) for x in line.split()]
            seats.append(l)
    return seats


def make_seating_chart(stlist, seats, shuffle=False):
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
    #print(stnum, seatsnum, W, seatH, rest)

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


def make_seat_pic(size, name):
    im = np.zeros((size[0] - 2, size[1] - 2), np.uint8) + 255
    cv2.putText(im, name, (10, 20), cv2.FONT_HERSHEY_PLAIN,
                1, (0, 0, 0), 1, cv2.LINE_AA)
    return im


def make_seats_pic(seats, PIC_INFO):
    w = PIC_INFO['MARGIN'] * 2
    h = PIC_INFO['MARGIN'] * 2
    for line in seats:
        h0 = PIC_INFO['WAY_H']
        if len(line) > 0:
            w += PIC_INFO['SEAT_SIZE'][1]
            for s in line:
                h0 += s * PIC_INFO['SEAT_SIZE'][0]
            h0 += PIC_INFO['WAY_H']
        else:
            w += PIC_INFO['WAY_W']
        if h < h0:
            h = h0
    #print(w, h)

    # 画像作成
    im = np.zeros((h, w), np.uint8) + 255
    # 教卓
    podium = (int(w/2) - PIC_INFO['SEAT_SIZE'][1], 5)
    t_podium = (podium[0] + PIC_INFO['SEAT_SIZE'][1] * 2,
                podium[1] + PIC_INFO['SEAT_SIZE'][0])
    cv2.rectangle(im, podium, t_podium, (0, 0, 0,), 4)
    #print(podium, t_podium)
    im_size = (PIC_INFO['SEAT_SIZE'][0], PIC_INFO['SEAT_SIZE'][1] * 2)
    #print(im_size)
    im[podium[1] + 1:t_podium[1] - 1, podium[0] + 1:t_podium[0] -
        1] = make_seat_pic(im_size, "   Teacher's Desk")

    target = [PIC_INFO['MARGIN'], PIC_INFO['WAY_H']]
    for line in seats:
        if len(line) > 0:
            for s in line:
                for i in range(s):
                    t = copy.copy(target)
                    t[0] += PIC_INFO['SEAT_SIZE'][1]
                    t[1] += PIC_INFO['SEAT_SIZE'][0]
                    cv2.rectangle(im, tuple(target), tuple(t), (0, 0, 0), 4)
                    target[1] = t[1]
                target[1] += PIC_INFO['WAY_H']
            target[0] += PIC_INFO['SEAT_SIZE'][1]
        else:
            target[0] += PIC_INFO['WAY_W']
        target[1] = PIC_INFO['WAY_H']
    return im


def make_chart_pic(im, chart, PIC_INFO):
    target = [PIC_INFO['MARGIN'], PIC_INFO['WAY_H']]
    for line in chart:
        if len(line) > 0:
            for s in line:
                for i in range(len(s)):
                    t = copy.copy(target)
                    t[0] += PIC_INFO['SEAT_SIZE'][1]
                    t[1] += PIC_INFO['SEAT_SIZE'][0]
                    im[target[1] + 1:t[1] - 1, target[0] + 1:t[0] - 1] = make_seat_pic(
                        PIC_INFO['SEAT_SIZE'], s[i])
                    target[1] = t[1]
                target[1] += PIC_INFO['WAY_H']
            target[0] += PIC_INFO['SEAT_SIZE'][1]
        else:
            target[0] += PIC_INFO['WAY_W']
        target[1] = PIC_INFO['WAY_H']
    cv2.imshow('im', im)
    cv2.waitKey()
    return im


def main():
    PIC_INFO = {
        'SEAT_SIZE': [30, 100],
        'WAY_H': 90,
        'WAY_W': 20,
        'MARGIN': 10,
    }

    title, stlist = make_title_and_stlist('list.txt')
    stnum = len(stlist)
    print(title, stnum)
    seats = make_seats('seats.txt')
    #print(seats)
    chart = make_seating_chart(stlist, seats, shuffle=True)
    # print(chart)
    chart_im = make_seats_pic(seats, PIC_INFO)
    chart_im = make_chart_pic(chart_im, chart, PIC_INFO)


if __name__ == '__main__':
    main()
