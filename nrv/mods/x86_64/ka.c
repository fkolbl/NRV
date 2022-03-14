/* Created by Language version: 7.7.0 */
/* VECTORIZED */
#define NRN_VECTORIZED 1
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "scoplib_ansi.h"
#undef PI
#define nil 0
#include "md1redef.h"
#include "section.h"
#include "nrniv_mf.h"
#include "md2redef.h"
 
#if METHOD3
extern int _method3;
#endif

#if !NRNGPU
#undef exp
#define exp hoc_Exp
extern double hoc_Exp(double);
#endif
 
#define nrn_init _nrn_init__ka
#define _nrn_initial _nrn_initial__ka
#define nrn_cur _nrn_cur__ka
#define _nrn_current _nrn_current__ka
#define nrn_jacob _nrn_jacob__ka
#define nrn_state _nrn_state__ka
#define _net_receive _net_receive__ka 
#define states states__ka 
 
#define _threadargscomma_ _p, _ppvar, _thread, _nt,
#define _threadargsprotocomma_ double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt,
#define _threadargs_ _p, _ppvar, _thread, _nt
#define _threadargsproto_ double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 /* Thread safe. No static _p or _ppvar. */
 
#define t _nt->_t
#define dt _nt->_dt
#define gbar _p[0]
#define shiftka _p[1]
#define ik _p[2]
#define p _p[3]
#define q _p[4]
#define ek _p[5]
#define g _p[6]
#define tau_q _p[7]
#define tau_p _p[8]
#define pinf _p[9]
#define qinf _p[10]
#define Dp _p[11]
#define Dq _p[12]
#define v _p[13]
#define _g _p[14]
#define _ion_ek	*_ppvar[0]._pval
#define _ion_ik	*_ppvar[1]._pval
#define _ion_dikdv	*_ppvar[2]._pval
 
#if MAC
#if !defined(v)
#define v _mlhv
#endif
#if !defined(h)
#define h _mlhh
#endif
#endif
 
#if defined(__cplusplus)
extern "C" {
#endif
 static int hoc_nrnpointerindex =  -1;
 static Datum* _extcall_thread;
 static Prop* _extcall_prop;
 /* external NEURON variables */
 extern double celsius;
 /* declaration of user functions */
 static void _hoc_rates(void);
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_prop_size(int, int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
extern Memb_func* memb_func;
 
#define NMODL_TEXT 1
#if NMODL_TEXT
static const char* nmodl_file_text;
static const char* nmodl_filename;
extern void hoc_reg_nmodl_text(int, const char*);
extern void hoc_reg_nmodl_filename(int, const char*);
#endif

 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _extcall_prop = _prop;
 }
 static void _hoc_setdata() {
 Prop *_prop, *hoc_getdata_range(int);
 _prop = hoc_getdata_range(_mechtype);
   _setdata(_prop);
 hoc_retpushx(1.);
}
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 "setdata_ka", _hoc_setdata,
 "rates_ka", _hoc_rates,
 0, 0
};
#define rates rates_ka
 extern double rates( _threadargsprotocomma_ double );
 /* declare global and static user variables */
#define A_tauq A_tauq_ka
 double A_tauq = 100;
#define A_taup A_taup_ka
 double A_taup = 5;
#define B_tauq B_tauq_ka
 double B_tauq = 0.035;
#define B_taup B_taup_ka
 double B_taup = 0.022;
#define C_tauq C_tauq_ka
 double C_tauq = 10.5;
#define C_taup C_taup_ka
 double C_taup = 2.5;
#define Q10TempB Q10TempB_ka
 double Q10TempB = 10;
#define Q10TempA Q10TempA_ka
 double Q10TempA = 22.85;
#define Q10ka Q10ka_ka
 double Q10ka = 1.93;
#define S0p5q S0p5q_ka
 double S0p5q = -7;
#define S0p5p S0p5p_ka
 double S0p5p = 28;
#define Vpq Vpq_ka
 double Vpq = -30;
#define V0p5q V0p5q_ka
 double V0p5q = -58;
#define Vpp Vpp_ka
 double Vpp = -65;
#define V0p5p V0p5p_ka
 double V0p5p = -28;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "Q10TempA_ka", "degC",
 "Q10TempB_ka", "degC",
 "V0p5p_ka", "mV",
 "S0p5p_ka", "mV",
 "A_taup_ka", "ms",
 "B_taup_ka", "/mV",
 "C_taup_ka", "ms",
 "Vpp_ka", "mV",
 "V0p5q_ka", "mV",
 "S0p5q_ka", "mV",
 "A_tauq_ka", "ms",
 "B_tauq_ka", "/mV",
 "C_tauq_ka", "ms",
 "Vpq_ka", "mV",
 "gbar_ka", "S/cm2",
 "shiftka_ka", "mV",
 "ik_ka", "mA/cm2",
 0,0
};
 static double delta_t = 0.01;
 static double p0 = 0;
 static double q0 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "Q10ka_ka", &Q10ka_ka,
 "Q10TempA_ka", &Q10TempA_ka,
 "Q10TempB_ka", &Q10TempB_ka,
 "V0p5p_ka", &V0p5p_ka,
 "S0p5p_ka", &S0p5p_ka,
 "A_taup_ka", &A_taup_ka,
 "B_taup_ka", &B_taup_ka,
 "C_taup_ka", &C_taup_ka,
 "Vpp_ka", &Vpp_ka,
 "V0p5q_ka", &V0p5q_ka,
 "S0p5q_ka", &S0p5q_ka,
 "A_tauq_ka", &A_tauq_ka,
 "B_tauq_ka", &B_tauq_ka,
 "C_tauq_ka", &C_tauq_ka,
 "Vpq_ka", &Vpq_ka,
 0,0
};
 static DoubVec hoc_vdoub[] = {
 0,0,0
};
 static double _sav_indep;
 static void nrn_alloc(Prop*);
static void  nrn_init(_NrnThread*, _Memb_list*, int);
static void nrn_state(_NrnThread*, _Memb_list*, int);
 static void nrn_cur(_NrnThread*, _Memb_list*, int);
static void  nrn_jacob(_NrnThread*, _Memb_list*, int);
 
static int _ode_count(int);
static void _ode_map(int, double**, double**, double*, Datum*, double*, int);
static void _ode_spec(_NrnThread*, _Memb_list*, int);
static void _ode_matsol(_NrnThread*, _Memb_list*, int);
 
#define _cvode_ieq _ppvar[3]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"ka",
 "gbar_ka",
 "shiftka_ka",
 0,
 "ik_ka",
 0,
 "p_ka",
 "q_ka",
 0,
 0};
 static Symbol* _k_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 15, _prop);
 	/*initialize range parameters*/
 	gbar = 0.000141471;
 	shiftka = 3;
 	_prop->param = _p;
 	_prop->param_size = 15;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 4, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_k_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[0]._pval = &prop_ion->param[0]; /* ek */
 	_ppvar[1]._pval = &prop_ion->param[3]; /* ik */
 	_ppvar[2]._pval = &prop_ion->param[4]; /* _ion_dikdv */
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 0,0
};
 static void _update_ion_pointer(Datum*);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, _NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _ka_reg() {
	int _vectorized = 1;
  _initlists();
 	ion_reg("k", -10000.);
 	_k_sym = hoc_lookup("k_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 1);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 15, 4);
  hoc_register_dparam_semantics(_mechtype, 0, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 ka /Users/louisregnacq/Dropbox/Work/Model/NRV/NRV/nrv/mods/ka.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static char *modelname = "";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static int _slist1[2], _dlist1[2];
 static int states(_threadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {int _reset = 0; {
   rates ( _threadargscomma_ v ) ;
   Dp = ( pinf - p ) / tau_p ;
   Dq = ( qinf - q ) / tau_q ;
   }
 return _reset;
}
 static int _ode_matsol1 (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
 rates ( _threadargscomma_ v ) ;
 Dp = Dp  / (1. - dt*( ( ( ( - 1.0 ) ) ) / tau_p )) ;
 Dq = Dq  / (1. - dt*( ( ( ( - 1.0 ) ) ) / tau_q )) ;
  return 0;
}
 /*END CVODE*/
 static int states (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) { {
   rates ( _threadargscomma_ v ) ;
    p = p + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / tau_p)))*(- ( ( ( pinf ) ) / tau_p ) / ( ( ( ( - 1.0 ) ) ) / tau_p ) - p) ;
    q = q + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / tau_q)))*(- ( ( ( qinf ) ) / tau_q ) / ( ( ( ( - 1.0 ) ) ) / tau_q ) - q) ;
   }
  return 0;
}
 
double rates ( _threadargsprotocomma_ double _lVm ) {
   double _lrates;
 tau_p = A_taup * exp ( - pow( ( B_taup ) , 2.0 ) * pow( ( _lVm - Vpp ) , 2.0 ) ) + C_taup ;
   pinf = 1.0 / ( 1.0 + exp ( ( _lVm - V0p5p + shiftka ) / ( - S0p5p ) ) ) ;
   tau_q = A_tauq * exp ( - pow( ( B_tauq ) , 2.0 ) * pow( ( _lVm - Vpq ) , 2.0 ) ) + C_tauq ;
   qinf = 1.0 / ( 1.0 + exp ( ( _lVm - V0p5q + shiftka ) / ( - S0p5q ) ) ) ;
   tau_p = tau_p * pow( Q10ka , ( ( Q10TempA - celsius ) / Q10TempB ) ) ;
   tau_q = tau_q * pow( Q10ka , ( ( Q10TempA - celsius ) / Q10TempB ) ) ;
   
return _lrates;
 }
 
static void _hoc_rates(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r =  rates ( _p, _ppvar, _thread, _nt, *getarg(1) );
 hoc_retpushx(_r);
}
 
static int _ode_count(int _type){ return 2;}
 
static void _ode_spec(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  ek = _ion_ek;
     _ode_spec1 (_p, _ppvar, _thread, _nt);
  }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
	double* _p; Datum* _ppvar;
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 2; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 }
 
static void _ode_matsol_instance1(_threadargsproto_) {
 _ode_matsol1 (_p, _ppvar, _thread, _nt);
 }
 
static void _ode_matsol(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  ek = _ion_ek;
 _ode_matsol_instance1(_threadargs_);
 }}
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_k_sym, _ppvar, 0, 0);
   nrn_update_ion_pointer(_k_sym, _ppvar, 1, 3);
   nrn_update_ion_pointer(_k_sym, _ppvar, 2, 4);
 }

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  int _i; double _save;{
  p = p0;
  q = q0;
 {
   rates ( _threadargscomma_ v ) ;
   p = pinf ;
   q = qinf ;
   }
 
}
}

static void nrn_init(_NrnThread* _nt, _Memb_list* _ml, int _type){
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v = _v;
  ek = _ion_ek;
 initmodel(_p, _ppvar, _thread, _nt);
 }
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _v){double _current=0.;v=_v;{ {
   g = gbar * pow( p , 3.0 ) * q ;
   ik = g * ( v - ek ) ;
   }
 _current += ik;

} return _current;
}

static void nrn_cur(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
  ek = _ion_ek;
 _g = _nrn_current(_p, _ppvar, _thread, _nt, _v + .001);
 	{ double _dik;
  _dik = ik;
 _rhs = _nrn_current(_p, _ppvar, _thread, _nt, _v);
  _ion_dikdv += (_dik - ik)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_ik += ik ;
#if CACHEVEC
  if (use_cachevec) {
	VEC_RHS(_ni[_iml]) -= _rhs;
  }else
#endif
  {
	NODERHS(_nd) -= _rhs;
  }
 
}
 
}

static void nrn_jacob(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml];
#if CACHEVEC
  if (use_cachevec) {
	VEC_D(_ni[_iml]) += _g;
  }else
#endif
  {
     _nd = _ml->_nodelist[_iml];
	NODED(_nd) += _g;
  }
 
}
 
}

static void nrn_state(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v = 0.0; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _nd = _ml->_nodelist[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v=_v;
{
  ek = _ion_ek;
 {   states(_p, _ppvar, _thread, _nt);
  } }}

}

static void terminal(){}

static void _initlists(){
 double _x; double* _p = &_x;
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = &(p) - _p;  _dlist1[0] = &(Dp) - _p;
 _slist1[1] = &(q) - _p;  _dlist1[1] = &(Dq) - _p;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif

#if NMODL_TEXT
static const char* nmodl_filename = "/Users/louisregnacq/Dropbox/Work/Model/NRV/NRV/nrv/mods/ka.mod";
static const char* nmodl_file_text = 
  ": Author: David Catherall; Grill Lab; Duke University\n"
  ": Created: November 2016\n"
  ": Ka is the Early Transient Outward K current in Schild 1994 \n"
  "\n"
  ": Neuron Block creates mechanism\n"
  "NEURON {\n"
  "       SUFFIX ka						:Sets suffix of mechanism for insertion into models\n"
  "       USEION k READ ek WRITE ik		:Lays out which NEURON variables will be used/modified by file\n"
  "       RANGE gbar, ek, ik, shiftka		:Allows variables to be modified in hoc and collected in vectors\n"
  "\n"
  "}\n"
  ": Defines Units different from NEURON base units\n"
  "UNITS {\n"
  "      (S) = (siemens)\n"
  "      (mV) = (millivolts)\n"
  "      (mA) = (milliamp)\n"
  "}\n"
  "\n"
  ": Defines variables which will have a constant value throughout any given simulation run\n"
  "	PARAMETER {\n"
  "		gbar =0.000141471 (S/cm2)	: (S/cm2) Channel Conductance\n"
  "		Q10ka=1.93 					:All gating variables have the same constant\n"
  "		Q10TempA = 22.85	(degC)			: Used to shift tau values based on temperature with equation : tau(T1)=tau(Q10TempA)*Q10^((Q10TempA-T1)/Q10TempB)\n"
  "		Q10TempB = 10	(degC)\n"
  "\n"
  "	 \n"
  "		shiftka=3.0 (mV) 			: Shift factor present in C-fiber\n"
  "		\n"
  "		:ka_p Variables\n"
  "			\n"
  "			: Steady State Variables\n"
  "				V0p5p=-28.0 (mV):As defined by Schild 1994, zinf=1.0/(1.0+exp((V-V0p5z)/(-S0p5z))\n"
  "				S0p5p=28.0 (mV)\n"
  "			\n"
  "			: Tau Variables\n"
  "				A_taup=5.0	(ms)	:As defined by Schild 1994, tauz=A_tauz*exp(-B^2(V-Vpz)^2)+C\n"
  "				B_taup=0.022	(/mV)\n"
  "				C_taup=2.5	(ms)\n"
  "				Vpp=-65.0		(mV)\n"
  "		\n"
  "		:ka_q Variables\n"
  "		\n"
  "			: Steady State Variables\n"
  "				V0p5q=-58.0 (mV)\n"
  "				S0p5q=-7.0 (mV)\n"
  "			\n"
  "			: Tau Variables\n"
  "				A_tauq=100.0	(ms)\n"
  "				B_tauq=0.035	(/mV)\n"
  "				C_tauq=10.5	(ms)\n"
  "				Vpq=-30.0	(mV)\n"
  "\n"
  "	}\n"
  "\n"
  ": Defines variables which will be used or calculated throughout the simulation which may not be constant. Also included NEURON provided variables, like v, celsius, and ina\n"
  "	ASSIGNED {\n"
  "\n"
  "		:NEURON provided Variables\n"
  "		 v	(mV) : NEURON provides this\n"
  "		 ik	(mA/cm2)\n"
  "		 celsius  (degC)\n"
  "		 ek	(mV)\n"
  "		 \n"
  "		 :Model Specific Variables\n"
  "		 g	(S/cm2)\n"
  "		 tau_q	(ms)\n"
  "		 tau_p	(ms)\n"
  "		 pinf\n"
  "		 qinf\n"
  "		 \n"
  "			 \n"
  "	}\n"
  "\n"
  ": Defines state variables which will be calculated by numerical integration\n"
  "	STATE { p q } \n"
  "\n"
  ": This block iterates the state variable calculations and uses those calculations to calculate currents\n"
  "	BREAKPOINT {\n"
  "		   SOLVE states METHOD cnexp\n"
  "		   g = gbar * p^3 * q\n"
  "		   ik = g * (v-ek)\n"
  "	}\n"
  "\n"
  ": Intializes State Variables\n"
  "	INITIAL {\n"
  "		rates(v) : set tau_m, tau_h, hinf, minf\n"
  "		: assume that equilibrium has been reached\n"
  "		\n"
  "\n"
  "		p = pinf\n"
  "		q = qinf\n"
  "	}\n"
  "\n"
  ":Defines Governing Equations for State Variables\n"
  "	DERIVATIVE states {\n"
  "		   rates(v)\n"
  "		   p' = (pinf - p)/tau_p\n"
  "		   q' = (qinf - q)/tau_q\n"
  "	}\n"
  "\n"
  ": Any other functions go here\n"
  "\n"
  "	:rates is a function which calculates the current values for tau and steady state equations based on voltage.\n"
  "		FUNCTION rates(Vm (mV)) (/ms) {\n"
  "			 tau_p = A_taup*exp(-(B_taup)^2*(Vm-Vpp)^2)+C_taup\n"
  "				 pinf = 1.0/(1.0+exp((Vm-V0p5p+shiftka)/(-S0p5p)))\n"
  "\n"
  "			 tau_q = A_tauq*exp(-(B_tauq)^2*(Vm-Vpq)^2)+C_tauq\n"
  "				 qinf = 1.0/(1.0+exp((Vm-V0p5q+shiftka)/(-S0p5q)))\n"
  "			\n"
  "			:This scales the tau values based on temperature\n"
  "			tau_p=tau_p*Q10ka^((Q10TempA-celsius)/Q10TempB)\n"
  "			tau_q=tau_q*Q10ka^((Q10TempA-celsius)/Q10TempB)\n"
  "		}\n"
  ;
#endif
