' Made by Jobry co.

Public Const ee As Double = 0.08181336998
Public Const Pi As Double = 3.1415926536

Function Power(ByVal Number As Double, PWR As Double) As Double
 If Number < 0 Then
  Exit Function
 Else
  Power = Exp(PWR * Log(Number))
 End If
End Function

Function Log10(ByVal Number As Double) As Double
 If Number <= 0 Then
  Exit Function
 Else
  Log10 = Log(Number) / Log(10)
 End If
End Function

Function Radians(ByVal Angle As Double) As Double
 Radians = Pi * Angle / 180
End Function

Function Degrees(ByVal Angle As Double) As Double
 Degrees = 180 * Angle / Pi
End Function

Function MCH(ByVal Angle As Double) As Double
  If (Angle < 0) Or (Angle > 89.9999999999) Then
  Exit Function
 Else
 A = Radians(Angle)
 MCH = 7915.70447 * Log10(Power(((1 - ee * Sin(A)) / (1 + ee * Sin(A))), (ee / 2)) * Tan(Pi / 4 + A / 2))
 If (Angle = 0) Then MCH = 0
 End If
End Function

Function AMCH(ByVal MPc As Double) As Double
 tc = 0
 td = 45
 ic = 45 / 2
 tc = MCH(td)
 While (Abs(tc - MPc) > 0.001)
  If (tc > MPc) Then td = td - ic Else td = td + ic
  tc = MCH(td)
  ic = ic / 2
 Wend
 AMCH = td
End Function

Function Course(ByVal dMP As Double, ByVal dLg As Double) As Double

 If (dMP <> 0) Then
  ct = Abs(Degrees(Atn(dLg / dMP)))
  ElseIf (dLg >= 0) Then ct = 90
  Else: ct = -90
  End If

 If dMP > 0 And dLg = 0 Then      'N
  Crs = 0
 ElseIf dMP > 0 And dLg > 0 Then  'NE
  Crs = ct
 ElseIf dMP = 0 And dLg > 0 Then  'E
  Crs = 90
 ElseIf dMP < 0 And dLg > 0 Then  'SE
  Crs = 180 - ct
 ElseIf dMP < 0 And dLg = 0 Then  'S
  Crs = 180
 ElseIf dMP < 0 And dLg < 0 Then  'SW
 Crs = 180 + ct
 ElseIf dMP = 0 And dLg < 0 Then  'W
  Crs = 270
 ElseIf dMP > 0 And dLg < 0 Then  'NW
  Crs = 360 - ct
 End If
 Course = Crs
End Function

Function Distance(ByVal dLt As Double, ByVal dMP As Double, ByVal dLg As Double, ByVal Lat As Double) As Double
 If dMP <> 0 Then
  OTS = dLt * dLg / dMP
  Else: OTS = dLg * Cos(Radians(Lat / 60))
  End If
  
 Distance = Sqr(dLt * dLt + OTS * OTS)
End Function
