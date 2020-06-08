function rolldice() {
  dice1 = Math.floor(Math.random() * 6) + 1;
  dice2 = Math.floor(Math.random() * 6) + 1;
  dice3 = Math.floor(Math.random() * 6) + 1;
  return dice1 + dice2 + dice3;
}

$(document).ready(function () {
  $("#rollstats").click(function () {
    $("#strength").val(rolldice());
    $("#dexterity").val(rolldice());
    $("#constitution").val(rolldice());
    $("#intelligence").val(rolldice());
    $("#wisdom").val(rolldice());
    $("#charisma").val(rolldice());
    $("#vocation").val();
  });
});
