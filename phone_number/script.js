	var DiE1	 = 0	 ;
	var DiE2		= 0 ;
 var SubTraCT		= false  ;
	let RESulT = document	 .getElementById  ("result"		) ;
 let InPuT	 = document	 .getElementById	 ("input"	 )  ;
		let dicETEXT	= document .getElementById	("dicetext"  )	;
  let iMg1	 = document	.getElementById		("img1"		)	;
	let Img2 = document  .getElementById	 ("img2"		)		;
 let REsuLtbUTtOnS		= document  .getElementsByClassName ("resultbutton"  )

	InPuT	.value	= "" ;


	InPuT  .onclick	= (	 )	=> { // can't turn off readonly now
 InPuT	 .readOnly	 = true	;	}
 InPuT	.onchange	 =  (  ) => { // now you really can't edit it
	InPuT	.readOnly	 = true	;
  InPuT	 .value		= ""	 ;	 }
  document  .body .onkeydown =	(  )	 =>	 { // now you REALLY can't edit it
	 InPuT	.readOnly	= true		; }

		function rollDice	(	 )	{
	 DiE1		= Math	 .floor	 (Math  .random  (		)	*6	 )  +1		;
	 DiE2	= Math  .floor		(Math	 .random  ( )  *6		)		+1  ;
	 if		(InPuT	.value === "123456789"  )	 {
	 DiE1	 = 1	 ;
	 DiE2 = 1  ;		}
		iMg1		.src	= "./static/images/"	 + DiE1 + ".jpeg"  ;
	 Img2	.src = "./static/images/"  + DiE2  + ".jpeg"	;
 SubTraCT = false	 ;
		dicETEXT	 .innerHTML	 = "You rolled a " + DiE1		+ " and a " + DiE2		+ ", for a result of "	 +	(SubTraCT	 ? Math  .abs (DiE1	 -DiE2	)  : (DiE1 + DiE2 )	) + "."
		for (let R of REsuLtbUTtOnS		) R	.style  .display	= "inline"	;
	 if	(1 == DiE1 == DiE2	 )		{
	dicETEXT	 .innerHTML = "Snake eyes! Your input has been reset."  ;
	InPuT	 .value	 = "" ;
 for  (let R of REsuLtbUTtOnS  ) R	 .style .display	= "none"	;	 }
	RESulT		.style  .display = "inline" ;	 }

  function addNumber	(	)  {
	InPuT	 .value  +=  (SubTraCT ? Math	 .abs (DiE1	 -DiE2	 )  : DiE1	+DiE2		)  ;
		RESulT		.style .display		= "none"	 ;		}
 async function submit  ( ) {
		if (!InPuT	 .value		)	{
	alert		("Please enter a phone number."	 )		;
 return  ;		}
		var c		= confirm	("Is "		+ InPuT  .value		+ " the correct phone number?"	)	;
 if		(!c ) return ;
	 await fetch	 ('/flag'		,	{
	 method : "POST" ,
	 body : InPuT		.value	 }	 ) .then ((res	) => res		.text		(	) )		.then	((text	)	=> text		.length !== 0		? document		.body	 .innerHTML		= text	 : alert  ("Sorry, incorrect."	 ) )		; }

		function setSubtract	 (	 )		{
	SubTraCT	= true	;
	dicETEXT .innerHTML		= "You rolled a "		+ DiE1  + " and a "	+ DiE2 + ", for a result of " +	 (SubTraCT	? Math  .abs  (DiE1	-DiE2		)	: (DiE1 + DiE2	 )  )	+ "."		;	 }
