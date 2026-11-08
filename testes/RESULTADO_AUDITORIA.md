Auditoria técnica automatizada.
Commit de origem: 068110440b0f3198d73f20aff00aa1d4af09b829
Python: success
Chromium: success

--- Logs dos testes Python ---
test_contagens_e_consistencia (test_pipeline.TesteIndicadores.test_contagens_e_consistencia) ... ok
test_dados_sao_agregados_sem_pii (test_pipeline.TesteIndicadores.test_dados_sao_agregados_sem_pii) ... ok
test_ponderacao_respostas (test_pipeline.TesteIndicadores.test_ponderacao_respostas) ... ok
test_html_offline_identico_ao_publico (test_publicacao.TestPublicacao.test_html_offline_identico_ao_publico) ... ok
test_pdf_v51_reproduzivel (test_publicacao.TestPublicacao.test_pdf_v51_reproduzivel) ... ok
test_scripts_ids_e_dados (test_publicacao.TestPublicacao.test_scripts_ids_e_dados) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.443s

OK
--- Logs do navegador ---
  File "/opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/site-packages/playwright/_impl/_frame.py", line 598, in _click
    await self._channel.send("click", self._timeout, locals_to_params(locals()))
  File "/opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/site-packages/playwright/_impl/_connection.py", line 78, in send
    return await self._connection.wrap_api_call(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/site-packages/playwright/_impl/_connection.py", line 636, in wrap_api_call
    raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
playwright._impl._errors.TimeoutError: Locator.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("#mobileMenu")
    - locator resolved to <button type="button" id="mobileMenu" class="mobile-menu" aria-label="Abrir menu">☰</button>
  - attempting click action
    2 × waiting for element to be visible, enabled and stable
      - element is not visible
    - retrying click action
    - waiting 20ms
    2 × waiting for element to be visible, enabled and stable
      - element is not visible
    - retrying click action
      - waiting 100ms
    58 × waiting for element to be visible, enabled and stable
       - element is not visible
     - retrying click action
       - waiting 500ms

