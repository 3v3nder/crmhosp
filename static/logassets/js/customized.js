$(".addtreat").click(function () {

    console.log("clicked");

    var treatcounts = document.getElementById('treatCount');

    treatcountsId = treatcounts.getAttribute('value');

    peerId = Number(treatcountsId ) + 1;

    treatcounts.value = peerId;

    console.log("treatcountsId" + treatcountsId);

    var treatvalue = document.getElementById('treatmen');

    treatvaluey =  treatvalue.options[treatvalue.selectedIndex].value;

    console.log("treatvalue" + treatvaluey);

    document.getElementById("treatlings").style.display = "block";

    const moretext = ( `
		<li>
        <span>Treatment:</span>
		${treatvalue.options[treatvalue.selectedIndex].text}
        <input type="hidden" class="form-control" name="treatment-${peerId}" id="treatment-${peerId}" value="${treatvaluey}" />
	</li>
  `);

  var remoteings = document.getElementById('treats');

  remoteings.innerHTML = remoteings.innerHTML +" " + moretext;
    
});