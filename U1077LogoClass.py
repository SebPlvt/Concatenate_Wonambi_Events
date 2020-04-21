# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 11:09:51 2019

@author: Sébastien Polvent
@mail: sebastien.polvent@unicaen.fr
@mail: seb6347@gmail.com
"""


class U1077_Logo():
    """prints the lab logo """
    def __init__(self):
        """ init class"""
        self.logo = "\n\n                    .Ns`       `o\n                    yMMN+.  `:sNM/\n              .  `/dMMMMMMMMMMMMMN.\n              yMMMMMMMmy+:...-:+hMm`\n              sMMMMMy-       `   .sm-\n             .NMMMy.      -ddyyds. -do`\n           .oNMMMs  :     mh   `Nd   /d+`\n          +MMMMMh  y/     yN-   `      +ds-\n           -NMMN` .M+      :syys+//::----yMdo.\n            +MM/  .Mm`         `.--:://+oymMMd.\n            sMN    yMd`                    .o-\n          -sMMy    `dMm.        `yMMMMs     `mMN-        Author : Sébastien Polvent\nymhs/.    `oNMd      :MMN.                         Contact : sebastien.polvent@unicaen.fr\n/MMMMMNh+`  .yM/      MMMy\n-yhdmMMMMMh/  -ho    -MMMh\n      `-/ohmm+`     .mMMM-     `-:::::::-`\n            `-:   `oNMMm:  .:::-``.-:--.`-:::.\n                -sNMMh/` :/-`:sdNMMMMMMMMdy/`-//\n             `+mMds:`  `/` /dNMMMMMMMMMMMMMMMh:`/:\n           `oms:              ./+:.`  `-+yNMMMMd-.o`\n          .h/     `/shmNysNmds/.          `/mMMMM/`o`\n          +     :hMMMMMM+oMMMMMMd/          `yMMMM:`o\n              .o....-MMM-/MMM/....+-          dMMMm +.\n             -Nh    `MMN :MMM:    oM/         +MMMM--/\n            `NMh    `MMm .MMM:    oMM-        +MMMM--/\n            +MMh    `MMh `MMM:    oMMy        hMMMN +.\n            sMMh    `MMy  NMM:    oMMh   `///yMMMMs/+///-  +////////o`o/////////\n            /MMh    `MMs  dMM:    oMMo.///` .NMMMm: /:/ -o o////+: `y`y////+` :+\n             dMd     dMs  yMN`    yMN``y+ys .NMms+ +- -o /:    -o :o      o- o:\n             `dM+    `//  :+`    -MN-  hMMy .m+`s- s`  s .o   -o :+      o- s.\n               oNh:            -sMy` `dMMNy .s///: o. .s :/  `y .s      :/ +-\n                `+dNdyo/   oydNmo.   ::-.-y .o   s``+/+``s`  +- s`      y `s\n                   `:oys   so/.    :::::-.h/+/    ///:///    y//s      .s/o-\n\n                       /h+   yh `ho  yh:   :hs  yh`  /h/\n                       sMNm- NM .Mh .MNN: :MNM  mM.  oMo\n                       sM++NoNM .Mh :MoyN/NoyM- mMdddmMo\n                       sM/ -mMM .Mh +M+ hMy sM: mM.  oMo\n                       /y:  `sy `yo /y-  `  :y: sy`  /y/\n\n\n"

    def print_logo(self):
        """ prints the logo"""
        print(self.logo, flush=True)

    def print_logo_with_delay(self):
        """ prints the logo"""
        import time
        for ligne in self.logo:
            print(ligne, end='', flush=True)
            time.sleep(0.001)
