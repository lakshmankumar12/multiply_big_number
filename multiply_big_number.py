#!/usr/bin/python

from __future__ import print_function
import sys

char_to_num={}

def init_char_to_num(char_to_num):
  for i in range(10):
    char_to_num[str(i)]=i

def direct_multiply(num1,l1,num2,l2):
  a=int(num1)
  b=int(num2)
  res=str(a*b)
  l = len(res)
  if l < l1+l2:
    res = "0" + res
  return res

def sum_big_num(num1, len_num1, num2, len_num2, carry_in):
  global char_to_num

  #pad both numbers to make them equi-length
  max_len = max(len_num1,len_num2)
  if len_num1 < max_len:
    num1 = "0" * (max_len-len_num1) + num1
  if len_num2 < max_len:
    num2 = "0" * (max_len-len_num2) + num2

  carry = carry_in
  s = ""
  for i in range(max_len-1,-1,-1):
    a = char_to_num[num1[i]]+char_to_num[num2[i]]+carry
    s = str(a%10) + s
    carry = a/10

  return (s,carry)


def multiply_big_number(num1, len_num1, num2, len_num2):

  #pad both numbers to make them equi-length
  max_len = max(len_num1,len_num2)

  if max_len <= 1:
    return direct_multiply(num1,max_len,num2,max_len)

  if max_len%2 == 1:
    max_len += 1
  if len_num1 < max_len:
    num1 = "0" * (max_len-len_num1) + num1
  if len_num2 < max_len:
    num2 = "0" * (max_len-len_num2) + num2


  msb_size = max_len/2
  lsb_size = max_len-msb_size  #lsb-split may be 1 higher or same as msb_size

  a = num1[:msb_size]
  b = num1[msb_size:]
  c = num2[:msb_size]
  d = num2[msb_size:]

  # (a + b) * (c + d) = ac + bc + ad + bd
  ac = multiply_big_number(a,msb_size,c,msb_size)
  bc = multiply_big_number(b,lsb_size,c,msb_size)
  ad = multiply_big_number(a,msb_size,d,lsb_size)
  bd = multiply_big_number(b,lsb_size,d,lsb_size)

  #cd      -> 2*lsb_size
  #(ad+bc) -> lsb+msb
  #ac      -> 2*msb_size

  (adbc,adbc_carry) = sum_big_num(ad,lsb_size+msb_size,bc,lsb_size+msb_size,0)
  #result has lsb_size of cd as-is.
  result = bd[lsb_size:]

  #sum msb of bd with lsb of (ad+bc)
  (second_part_sum,second_part_carry) = sum_big_num(bd[:lsb_size],lsb_size,adbc[msb_size:],lsb_size,0)
  result = second_part_sum + result

  #sum lsb of ac with msb of (ad+bc)
  (third_part_sum,third_part_carry) = sum_big_num(ac[msb_size:],msb_size,adbc[:lsb_size],msb_size,second_part_carry)
  result = third_part_sum + result

  (forth_part_sum,discard) = sum_big_num(ac[:msb_size],msb_size,"",0,third_part_carry+adbc_carry)
  result = forth_part_sum + result

  while len(result) > len_num1 + len_num2:
    if result[0] != "0":
      sys.exit("issue");
    result = result[1:]

  return result

if __name__ == '__main__':
  init_char_to_num(char_to_num)

  try:
    b = int(sys.argv[1])
    n = int(sys.argv[2])
  except Exception,e:
    print("Usage: %s <base> <power-required>")
    print("Got error in parsing:%s"%str(e))
    sys.exit(1)

  if n > 255:
    print("You should increase the power. Max supported is 255")
    sys.exit(1);

  powers = {}
  max_powers=8
  powers[0] = str(b)
  for i in range(1,max_powers):
    s = powers[i-1]
    l = len(s)
    p = multiply_big_number(s,l,s,l)
    while p[0] == "0":
      p = p[1:]
    powers[i] = p
  print("printing powers")
  for i in range(0,max_powers):
    print("power of %d to %d is %s"%(b,1<<i,powers[i]))
  result_so_far = "1"
  for i in range(max_powers-1,-1,-1):
    ipow2 = 1<<(i)
    if n >= ipow2:
      print("%s is more or equal than %d, so multiplying this power %d"%(n,ipow2,i))
      result_so_far = multiply_big_number(result_so_far,len(result_so_far),powers[i],len(powers[i]))
      while result_so_far[0] == "0":
        result_so_far = result_so_far[1:]
      n -= ipow2
  print ("%d raised to %s is %s"%(b,sys.argv[2],result_so_far))

