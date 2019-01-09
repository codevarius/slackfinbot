/*
script generates rgb color from delta between sales  of pesent month and past month
*/
//depricated
function randRGB(d,max,min) {

    var std_cahnge = d.data['std_value'] - d.data['std_pvalue']
    
    if(std_cahnge != 0 && std_cahnge > 0){
        //console.log((d.data['change']/max) * 100)
        return perc2color((std_cahnge/max));
    }else if(std_cahnge != 0 && std_cahnge < 0){
        //console.log((d.data['change']/Math.abs(min)) * 100)
        return perc2color((std_cahnge/Math.abs(min)));
    }else if(std_cahnge == 0 && d.data['name'] != "Рынок"){
        return'rgb(150,150,150)';
    }else{
        return'rgb(255,255,255)'; 
    }
}
//depricated
//dig out max and min value from root
function getMinMax(root) {
    var valList = [];
    root.forEach(element => {
        if(element.data['std_value'] != undefined) //change element tag later
            valList.push(element.data['std_value'] - element.data['std_pvalue'])
    });
    max = Math.max.apply(null, valList)
    min = Math.min.apply(null, valList)
    return {'max':max,'min':min};
}

//produce rgb
function perc2color(perc) {

    var r = 150;
    var g = 150;
    var b = 150;
	if(perc < 0 && perc != -Infinity) {
		r = 255;
        g = Math.round(150 * (1-Math.abs(perc)));
        b = Math.round(150 * (1-Math.abs(perc)));
	}else if(perc > 0 && perc != Infinity){
		g = 255;
        r = Math.round(150 * (1-Math.abs(perc)));
        b = Math.round(150 * (1-Math.abs(perc)));
    }else if(perc == Infinity){
        r = 0;
        g = 255;
        b = 0;
    }else if(perc == -Infinity){
        r = 255;
        g = 0;
        b = 0;
    }
    //console.log("rgb("+r+","+g+","+b+")")
	return "rgb("+r+","+g+","+b+")"
}