#!/bin/bash


b64_txt='VmxSR1lWUXhTa2hXYWxwV1ZrVkthRlpyVm1GamJHUlhWV3RhVG1FemFGWldWbWhyVjJ4YVNGUnFRbFZoTVVwVFdsZHpOVlpGTVZoaVJuQlhUVVJGZWxaRldtdFVNa3BIWWtoR1YySlhlRTlaVjNSTFlqRmtjMVZzU2s5U1ZFWmFWRlZSZDFCUlBUMD0='

echo $b64_txt | base64 -d | base64 -d | base64 -d | base64 -d | base64 -d 
# ISC{44e1da16-40a7-4439-bac0-ceb5b20ae481}