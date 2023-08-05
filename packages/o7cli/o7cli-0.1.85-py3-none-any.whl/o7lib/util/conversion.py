#!/usr/bin/python
#************************************************************************
# Copyright 2021 O7 Conseils inc (Philippe Gosselin)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#************************************************************************
import math



#*************************************************
#
#*************************************************
def SpeedUVToWs(u,v):
    return math.sqrt( (u ** 2) + (v ** 2) )



#*************************************************
#
#*************************************************
def SpeedMsToKnot(ms):
    return ms * 1.944


#*************************************************
#
#*************************************************
def DirectionUVToDeg(u,v):
    rad = math.atan2(u * -1., v * -1.)
    deg = (rad * 180.) / math.pi
    if deg < 0 : deg += 360
    
    return deg


#*************************************************
#
#*************************************************
def DirectionDegToTxt(deg):
    txt = [ 'N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSO', 'SO', 'OSO', 'O', 'ONO', 'NO', 'NNO']
    i = round((deg / 360) * 16)
    if i >= 16: i = 0
    return txt[i]



#*************************************************
#
#*************************************************
if __name__ == "__main__":


    for d in range(0,360):
        print(f'{d} -> {DirectionDegToTxt(d)}')

 
   