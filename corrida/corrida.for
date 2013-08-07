      program corrida
      implicit none
      real*8 x(27),pvm(10),phr(10),y,t,d,p,s,v,vm
      real*8 vo2,pvmax,vo2max,phrmax,hrmax,hr
      real*8 estd,estt,t1(10,27),r1(10,27)
      integer*4 hh1(10,27),mm1(10,27),ss1(10,27)
      integer*4 rh1(10,27),rm1(10,27),rs1(10,27)
      integer*4 hh,mm,ss
      integer*4 i,j
      character*1 co,ps,sc
      character*10 name
      write(*,*)'Entre o seu nome'
      read(*,'(a10)')name
      write(*,*)'Entre a sua idade'
      read(*,*)y
      write(*,*)'Entre com a distancia base em m'
      read(*,*)d
      write(*,*)'Entre com o tempo HH:MM:SS'
      read(*,'(i2,1x,i2,1x,i2)')hh,mm,ss

      t=float(hh)*60.+float(mm)+float(ss)/60
      co=':'
      sc=','
      ps='%'
      
      do i=1,10
         pvm(i)=0.55+0.05*(float(i))
         phr(i)=0.63*pvm(i)+0.37
      end do

      x(1)=100.
      x(2)=120.
      x(3)=150.
      x(4)=200.
      x(5)=300.
      x(6)=400.
      x(7)=500.
      x(8)=600.
      x(9)=667.
      x(10)=800.
      x(11)=1000.
      x(12)=1200.
      x(13)=1500.
      x(14)=1600.
      x(15)=2000.
      x(16)=3000.
      x(17)=5000.
      x(18)=6000.
      x(19)=7000.
      x(20)=8000.
      x(21)=10000.
      x(22)=12000.
      x(23)=15000.
      x(24)=18000.
      x(25)=20000.
      x(26)=42195./2.
      x(27)=42195.

      v=vo2(t,d)
      p=pvmax(t)
      vm=vo2max(v,p)

      hrmax= 206.3 - (0.711 * y)
      phrmax=.63*p+.37
      hr=phrmax*hrmax
      do j=1,27
         do i=10,1,-1
            t1(i,j)=60*estt(x(j),pvm(i)*vm)
            call d2hms(t1(i,j),hh1(i,j),mm1(i,j),ss1(i,j))
            r1(i,j)=1000.*t1(i,j)/x(j)            
            call d2hms(r1(i,j),rh1(i,j),rm1(i,j),rs1(i,j))
         end do
      end do
      open(9,file='corrida.csv',status='unknown')
      write(9,'(a9,a10)')'Atleta:, ',name
      write(9,'(a9,i2,a6)')'Idade:, ',int(y),',anos'
      write(9,'(a17,f8.1,a2)')'Distancia,base:,',d,',m'
      write(9,'(a13,i2.2,1a,i2.2,1a,i2.2)')'Tempo,base:,',hh,co,mm,co,ss
      write(9,*)' '
      write(9,'(a15,i3,a10)')'VO2,estimado:,',Nint(v),',ml/kg/min'
      write(9,'(a15,i3,a18,i3,a10)')'Equivalente,a,',Nint(p*100),
     $     '%,do,VO2,maximo:,',Nint(vm),',ml/kg/min'
      write(9,*)' '
      write(9,'(a17,i3,a4)')'Ritmo,cardiaco:,', Nint(hr),',bpm'
      write(9,'(a15,i3,a28,i3,a4)')'Equivalente,a,',Nint(phrmax*100),
     $     '%,do,ritmo,cardiaco,maximo:,',Nint(hrmax),',bpm'
      write(9,*)' '
      write(9,*)'Tempos,Estimados,e,%VO2,Max '
      write(9,'(a9,10(1a,4x,i3,1a))')'Distancia',
     $     (sc,Nint(pvm(i)*100),ps,i=10,1,-1)
      write(9,*)' '
      write(9,'(27(f8.1,10(1a,i2.2,1a,i2.2,1a,i2.2),/))')
     $ (x(j),(sc,hh1(i,j),co,mm1(i,j),co,ss1(i,j),i=10,1,-1),j=1,27)
      write(9,*)'Ritmos,Estimados,e,%Max,Ritmo,Cardiaco '
      write(9,'(a9,10(1a,4x,i3,1a))')'Distancia',
     $     (sc,Nint(phr(i)*100),ps,i=10,1,-1)
      write(9,*)' '
      write(9,'(27(f8.1,10(1a,i2.2,1a,i2.2,1a,i2.2),/))')
     $ (x(j),(sc,rh1(i,j),co,rm1(i,j),co,rs1(i,j),i=10,1,-1),j=1,27)
      write(9,*)' '
      close(9)

      end

      subroutine d2hms(t,hh,mm,ss)
      implicit none
      real*8 t
      integer*4 hh,mm,ss
      hh=int(t/3600.)
      mm=int(t/60-float(hh*60) )
      ss=Nint(t-float(mm*60)-float(hh*3600))
      return
      end

      function vo2(t,d)
      implicit none
      real*8 t,d,s,a,b,r,vo2
      a=-4.60
      b=0.182258
      r=0.000104
      s=d/t
      vo2=(a+b*s+r*s**2)
      return
      end

      function pvmax(t)
      implicit none
      real*8 d,e,f,g,h,t,pvmax
      d=0.8
      e=0.1894393
      f=-0.012778
      g=0.2989558
      h=-0.1932605
      pvmax=(d+e*exp(f*t)+g*exp(h*t))
      return
      end

      function vo2max(v,p)
      implicit none
      real*8 v,p,vo2max
      vo2max=v/p
      return
      end

      function estt(estd,vm)
      implicit none
      real*8 vm,vo2,pvmax,vo2max,eps,aeps,t1,v1,p1,vm1,dt
      real*8 estd,estt
      estt=estd/50
      dt=estt/2
      aeps=9999
      do while(aeps.gt.1e-6)
         v1=vo2(estt,estd)
         p1=pvmax(estt)
         vm1=vo2max(v1,p1)
         eps=vm1-vm
         aeps=abs(eps)
         if(eps.gt.1e-6)then ! increase estt
            estt=estt+dt
         elseif(eps.lt.-1e-6)then ! decrese estt
            estt=estt-dt
         end if
         dt=dt/2
      end do
      return
      end

