#include "itensor/all.h"
#include<map>
using namespace itensor;

int 
main()
{
  int N = 3;

  auto sites = SpinOne(N,{"ConserveQNs=",false});
  std::map<int,int> weights;
  weights[1]=15;
  weights[2]=20;
  weights[3]=25;
  double gamma=1;
  auto ampo = AutoMPO(sites);
  for(int j = 1; j <= N; ++j)
    {
      ampo += (0.5*weights[j]-gamma),"Sz",j;
            ampo += (0.5*weights[j]+gamma),"Id",j;
  for(int i = 1; i <= N; ++i)
    {
      if(i!=j)
	{
      ampo += gamma,"Sz",j,"Sz",i;
	}
    }
    }
  auto H = toMPO(ampo);

  auto sweeps = Sweeps(25);
  sweeps.maxdim() = 10,20,100,100,200;
  sweeps.cutoff() = 1E-10;
  sweeps.niter() = 2;
  sweeps.noise() = 1E-7,1E-8,0.0;  

  auto psi0 = randomMPS(sites);

  auto [energy,psi] = dmrg(H,psi0,sweeps);

  println("Ground State Energy = ",energy);
  for( auto j : range1(N) ) 
    {
      //re-gauge psi to get ready to measure at position j
      psi.position(j);

      auto ket = psi(j);
      auto bra = dag(prime(ket,"Site"));

      auto Szjop = op(sites,"Sz",j);

      //take an inner product 
      auto szj = elt(bra*Szjop*ket);
      printfln("%d %.12f",j,szj);
        
    }
  return 0;
}
