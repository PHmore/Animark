function minhaFuncao1()
{
    window.alert("Uma mensagem");
    $('.btn-danger').empty().append('Novo nome btt').css({color: '#00ff00', textTransform: 'uppercase', width: '70fr'});
    $('#area-mensagens').empty().append('Area de Mensagens');
}

function minhaFuncao2()
{
    // O $ representa o objeto Jquery

    // Remove os elementos filhos daquele id
    $('#area-mensagens').empty();

    var alunos = ['Aluno 1', 'Aluno 2', 'Aluno 3', 'Aluno 4', 'Aluno 5'];

    // Itera ao longo do array inserindo seus elementos ao final daquela cujo
    // Aparentemente foi declarado uma função dentro de um argumento de função
    $.each(alunos, 
        function(index, value){
        $('#area-mensagens').append(value);
    }
    ); 
    $('.btn-danger').empty().append('Executar');
}