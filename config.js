// ============================================================
// CONFIGURAÇÃO DO DASHBOARD - Feira de Mercado
// ------------------------------------------------------------
// Este é o ÚNICO arquivo que você precisa editar. Preencha os
// dois valores abaixo seguindo o LEIA-ME.md, salve e envie
// para o GitHub. O resto do dashboard usa isto automaticamente.
// ============================================================

window.FEIRA_CONFIG = {

  // 1) ID DA PLANILHA GOOGLE SHEETS
  // -----------------------------------------------------------
  // Cole aqui só o pedaço do ID que fica no meio da URL.
  // Exemplo: se sua URL for
  //   https://docs.google.com/spreadsheets/d/1AbCdEfG_xxxxxxxxxxxxxxx-yyy/edit
  // então SHEET_ID = "1AbCdEfG_xxxxxxxxxxxxxxx-yyy"
  //
  // IMPORTANTE: a planilha precisa estar compartilhada como
  // "Qualquer pessoa com o link - Leitor" (Anyone with the link - Viewer).
  //
  SHEET_ID: "1uS8PLkOZdRIRdNjZ7UrGGLHDbMMIowLA",


  // 2) CLIENT ID DO GOOGLE OAUTH (para a trava de email)
  // -----------------------------------------------------------
  // Você cria isso uma única vez em console.cloud.google.com
  // (passo a passo no LEIA-ME.md). Formato:
  //   123456789012-abc...xyz.apps.googleusercontent.com
  //
  OAUTH_CLIENT_ID: "536199512837-hnmkhr00av1goag68a6o62mivth1jtdm.apps.googleusercontent.com",


  // 3) DOMÍNIO PERMITIDO (só emails deste domínio entram)
  // -----------------------------------------------------------
  ALLOWED_DOMAIN: "eescjr.com.br",


  // 4) OPÇÕES AVANÇADAS (pode deixar como está)
  // -----------------------------------------------------------
  // Se true, o dashboard funciona sem login e usa data.json
  // (modo offline / para testes locais).
  OFFLINE_MODE: false,

  // Recarregar dados da planilha a cada X minutos (0 = desligado)
  AUTO_REFRESH_MIN: 10,
};
