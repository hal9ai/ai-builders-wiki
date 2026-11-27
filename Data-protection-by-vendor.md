---
title: "Data protection by vendor"
description: "Training defaults, opt-outs, retention, zero data retention and data location for each major AI vendor, every cell sourced."
category: Security and data
tags: [privacy, providers]
order: 3
checked: 2026-10-28
---

<!-- NAV:START -->
[Home](README.md) › [Security and data](Category-Security-and-data.md) · Tags: [privacy](Tag-privacy.md), [providers](Tag-providers.md)
<!-- NAV:END -->

# Data protection by vendor

**This page compares what the main AI vendors do with your data, plan by plan, with every answer linked to the vendor's own page as checked on 2026-10-28, except the Cohere, Groq, xAI and DeepSeek API rows, checked on 2026-11-27.** For what the questions mean and what to do about them, start with [Data protection when you use AI](Data-protection.md).

**This is not legal advice.** It summarizes public vendor pages to help you ask the right questions. Policies change often, your contract may say something different, and laws such as the GDPR put obligations on *you* as the app maker. For a real decision, read the current terms and ask a lawyer or your data protection officer.

## Comparison table

Short answers; the linked page has the exact wording. "Not stated" means we did not find it on the vendor's pages on the check date, not that it does not exist. Pages marked † refused automated access on 2026-10-28; their cells rest on the page text as shown in search results, and need a manual check.

| Vendor and plan | Trains on your data by default? | Opt-out | Default retention | Zero data retention | Location / EU option |
|---|---|---|---|---|---|
| **Anthropic**: Claude Free, Pro, Max | Only if you allow it; you choose at signup or in settings ([news](https://www.anthropic.com/news/updates-to-our-consumer-terms)) | Privacy Settings, any time ([news](https://www.anthropic.com/news/updates-to-our-consumer-terms)); Incognito chats never used ([help](https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training)) | 30 days if training is off; 5 years if on ([news](https://www.anthropic.com/news/updates-to-our-consumer-terms)); deleted chats removed from back-end within 30 days ([help](https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data)) | No ([help](https://privacy.claude.com/en/articles/8956058-i-have-a-zero-data-retention-agreement-with-anthropic-what-products-does-it-apply-to)) | Not stated |
| **Anthropic**: API, Claude for Work | No ([help](https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training)) | Not needed; feedback you submit may be used (same page) | API inputs and outputs deleted within 30 days ([help](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data)) | Some API and Claude Code for Enterprise customers, on approval ([help](https://privacy.claude.com/en/articles/8956058-i-have-a-zero-data-retention-agreement-with-anthropic-what-products-does-it-apply-to)) | Inference "us" or "global" (default); storage US only; no EU option ([docs](https://platform.claude.com/docs/en/manage-claude/data-residency)) |
| **OpenAI**: ChatGPT Free, Plus, Pro | Yes ([help](https://help.openai.com/en/articles/5722486-how-your-data-is-used-to-improve-model-performance) †) | "Improve the model for everyone" in Data controls (same page †) | Deleted chats scheduled for deletion within 30 days ([help](https://help.openai.com/en/articles/8983778-chat-and-file-retention-in-chatgpt) †); Temporary Chat copies up to 30 days ([help](https://help.openai.com/en/articles/8914046-temporary-chat-in-chatgpt) †) | Not stated for consumer plans | Not stated |
| **OpenAI**: ChatGPT Business, Enterprise, Edu | No, unless the organization agrees otherwise ([help](https://help.openai.com/en/articles/5722486-how-your-data-is-used-to-improve-model-performance) †) | Not needed | Not stated (page †) | Not stated | Not stated |
| **OpenAI**: API | No, unless you opt in ([docs](https://developers.openai.com/api/docs/guides/your-data)) | Not needed | Abuse-monitoring logs up to 30 days; Responses API state 30 days by default (same page) | On approval (same page) | Regions incl. Europe (EEA + Switzerland); non-US regions need approval and a contract amendment (same page) |
| **Google**: Gemini app | Yes ([Privacy Hub](https://support.google.com/gemini/answer/13594961?hl=en)) | Turn off Keep Activity (same page) | Auto-delete after 18 months by default (3, 36 months or never); 72 hours with Keep Activity off; reviewed chats up to 3 years (same page) | Not applicable | Provided by Google Ireland in the EEA and Switzerland; storage location not stated (same page) |
| **Google**: Gemini API, unpaid | Yes; human reviewers may read inputs and outputs ([terms](https://ai.google.dev/gemini-api/terms)) | Use the paid tier (same page) | Abuse monitoring: 55 days ([policy](https://ai.google.dev/gemini-api/docs/usage-policies)) | No | In the EEA, UK and Switzerland, paid terms apply to all use ([terms](https://ai.google.dev/gemini-api/terms)) |
| **Google**: Gemini API, paid | No ([terms](https://ai.google.dev/gemini-api/terms)) | Not needed | Abuse monitoring: 55 days ([policy](https://ai.google.dev/gemini-api/docs/usage-policies)); logs on by default for projects created since 2026-10-26, kept 55 days by default ([logs](https://ai.google.dev/gemini-api/docs/logs-policy)) | You configure it by avoiding storing features; some features always store ([ZDR](https://ai.google.dev/gemini-api/docs/zdr)) | Not stated |
| **Google Cloud**: Vertex AI | No, without your permission ([docs](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/data-governance)) | Not needed | Cache deleted within 24 hours; prompts may be logged for abuse detection (same page) | You configure it (disable logging and caching) (same page) | Choose a region; `eu` endpoint keeps data in EU member states ([residency](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/data-residency)) |
| **Microsoft**: Azure OpenAI in Foundry | No, without your permission; not available to OpenAI ([docs](https://learn.microsoft.com/en-us/azure/ai-foundry/responsible-ai/openai/data-privacy)) | Not needed | Flagged content may be stored for abuse review; period not stated (same page) | Modified abuse monitoring, by application ([docs](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/abuse-monitoring)) | Your chosen geography, unless Global or DataZone deployment; EU DataZone available ([docs](https://learn.microsoft.com/en-us/azure/ai-foundry/responsible-ai/openai/data-privacy)) |
| **Mistral**: Vibe (consumer chat app) | Yes ([help](https://help.mistral.ai/en/articles/347617-do-you-use-my-user-data-to-train-your-artificial-intelligence-models)) | Toggle in settings or admin panel ([help](https://help.mistral.ai/en/articles/455207-can-i-opt-out-of-my-input-or-output-data-being-used-for-training)) | Until you delete the conversation or account ([privacy policy](https://legal.mistral.ai/terms/privacy-policy)) | No ([help](https://help.mistral.ai/en/articles/347612-can-i-activate-zero-data-retention-zdr)) | EU by default ([help](https://help.mistral.ai/en/articles/347629-where-do-you-store-my-data-or-my-organization-s-data)) |
| **Mistral**: Enterprise | No, opted out by default ([help](https://help.mistral.ai/en/articles/347617-do-you-use-my-user-data-to-train-your-artificial-intelligence-models)) | Not needed | Not stated | No; ZDR is for pay-as-you-go API calls only ([help](https://help.mistral.ai/en/articles/347612-can-i-activate-zero-data-retention-zdr)) | EU by default ([help](https://help.mistral.ai/en/articles/347629-where-do-you-store-my-data-or-my-organization-s-data)) |
| **Mistral**: API | Free mode: may be used; pay-as-you-go: you can opt out, default not stated ([help](https://help.mistral.ai/en/articles/347617-do-you-use-my-user-data-to-train-your-artificial-intelligence-models)) | Admin panel toggle ([help](https://help.mistral.ai/en/articles/455207-can-i-opt-out-of-my-input-or-output-data-being-used-for-training)) | 30 rolling days for abuse monitoring, except specific APIs ([privacy policy](https://legal.mistral.ai/terms/privacy-policy)) | Pay-as-you-go, stateless calls only, at Mistral's discretion ([help](https://help.mistral.ai/en/articles/347612-can-i-activate-zero-data-retention-zdr)) | EU by default; US endpoint optional ([help](https://help.mistral.ai/en/articles/347629-where-do-you-store-my-data-or-my-organization-s-data)) |
| **Cohere**: SaaS Platform | Unless you opt out: the page describes a Data Controls opt-out, not a default, and the commitments cover "enterprise data of our commercial, paying customers" ([commitments](https://cohere.com/enterprise-data-commitments)) | Settings → Data Controls: "Adjust the toggle to 'Off' to opt out"; the change applies to data created afterwards (same page) | Logged prompts and generations are automatically deleted after 30 days, with exceptions (same page) | Approved enterprise customers: "we do not log any prompts or generations" (same page) | Not stated |
| **Groq**: API | No: Groq is "not permitted to use Inputs or Outputs for training or fine-tuning any AI Model Services or other models" unless the customer permits it ([agreement §4.2](https://console.groq.com/docs/legal/services-agreement)) | Not needed | "By default, Groq does not retain customer data for inference requests"; inputs and outputs may be logged "up to 30 days" for reliability or abuse investigations ([your data](https://console.groq.com/docs/your-data)) | Self-serve for all customers; features that need stored data are disabled ([your data](https://console.groq.com/docs/your-data)) | Not stated |
| **xAI**: API | No: "SpaceXSI never trains on your API inputs or outputs without your explicit permission" ([security FAQ](https://docs.x.ai/developers/faq/security)) | Not needed | API requests and responses stored encrypted at rest for 30 days, then deleted (same page) | Team-wide, self-serve where available; prompts and outputs are "never persisted to disk" (same page) | Not stated |
| **Meta**: Meta AI app | Yes ([help](https://www.meta.com/help/artificial-intelligence/)) | In the EU, an objection form ([Meta newsroom](https://about.fb.com/news/2025/04/making-ai-work-harder-for-europeans/)); elsewhere not stated | Not stated | Not applicable | Not stated |
| **DeepSeek**: app | Yes, after de-identification ([terms](https://cdn.deepseek.com/policies/en-US/deepseek-terms-of-use.html)) | "Improve the model for everyone" setting (same page) | As long as you have an account ([privacy policy](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html)) | Not stated | Stored in the People's Republic of China (same page) |
| **DeepSeek**: API | Yes by default: DeepSeek says it may use inputs and outputs to develop, train, evaluate and improve its models unless a separate written agreement says otherwise ([Open Platform privacy policy](https://cdn.deepseek.com/policies/zh-CN/deepseek-open-platform-privacy-policy.html), effective 2026-11-11; the English page returned 404) | No self-service API opt-out; a separate written agreement is the stated exception (same page) | No fixed period; network logs kept at least six months (same page) | Not offered (same page) | Stored in mainland China (same page) |
| **Any open-weight model you run yourself** | Only what you do | Not applicable | What you configure | Yes, if you store nothing | Wherever you run it |

All vendor pages were checked on 2026-10-28, except the Cohere, Groq, xAI and DeepSeek API rows, checked on 2026-11-27. † = page refused automated access; manual check needed.

## Details and exact wording, by vendor

### Anthropic

- **Consumer training is a choice.** The update gives "users the choice to allow their data to be used to improve Claude"; "You're always in control of this setting"; new users "can select your preference in the signup process" ([news](https://www.anthropic.com/news/updates-to-our-consumer-terms)). The page does not say which way the switch starts.
- **Consumer retention.** If you allow training, retention is extended "to five years"; otherwise the "30-day data retention period" applies (same page). For conversations flagged by safety systems: "We retain inputs and outputs for up to 2 years and trust and safety classification scores for up to 7 years" ([help](https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data)).
- **Commercial.** "By default, we will not use your inputs or outputs from our commercial products" to train ([help](https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training)). For the [API](Glossary.md#api), "we automatically delete inputs and outputs on our backend within 30 days of receipt or generation", with exceptions such as [ZDR](Glossary.md#zero-data-retention-zdr) agreements and the Files API ([help](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data)).
- **Location.** "Inference geo: Only `"us"` and `"global"` are available", and "Workspace geo: Only `"us"` is currently available" ([data residency](https://platform.claude.com/docs/en/manage-claude/data-residency)). Through Amazon Bedrock or Google Cloud, those platforms' own regional options apply instead.

### OpenAI

- **API.** "data sent to the OpenAI API is not used to train or improve OpenAI models", unless "you explicitly opt in"; "abuse monitoring logs are generated for all API feature usage and retained for up to 30 days"; ZDR and modified abuse monitoring are "subject to prior approval by OpenAI" ([Your data](https://developers.openai.com/api/docs/guides/your-data)). Data residency regions include "Europe (EEA + Switzerland)"; some regions store data at rest only, without regional processing (same page).
- **ChatGPT consumer and business.** OpenAI's help center refused automated access on 2026-10-28. As indexed by search, it says: "When you use our services for individuals (Free, Plus, Pro), we may use your content to train our models", with an opt-out in Data controls ([help](https://help.openai.com/en/articles/5722486-how-your-data-is-used-to-improve-model-performance) †). Check these pages yourself in a browser.
- **Court-ordered retention.** OpenAI has published statements about a US court case that required it to keep some ChatGPT and API data longer than usual. We could not open those pages on 2026-10-28, so we do not summarize them here. If this matters for you, read [OpenAI's statement](https://openai.com/index/response-to-nyt-data-demands/) † directly.

### Google

- **Gemini app.** "Google uses your activity to provide, develop, and improve its services (including training generative AI models)"; "To stop your future chats from being reviewed to improve Google services, turn off your Keep Activity setting"; "Temporary chats and chats you have when Keep Activity is off are retained with your account for 72 hours"; "Reviewed chats are retained for up to three years" ([Gemini Apps Privacy Hub](https://support.google.com/gemini/answer/13594961?hl=en)). Work and school accounts "may be subject to different data handling terms" (same page).
- **Gemini API.** On unpaid services, Google "uses the content you submit … to provide, improve, and develop" its products and "human reviewers may read, annotate, and process your API input and output"; on paid services, "Google doesn't use your prompts … or responses to improve our products" ([Gemini API terms](https://ai.google.dev/gemini-api/terms)). For abuse monitoring, "Google retains the following data for fifty-five (55) days" ([usage policies](https://ai.google.dev/gemini-api/docs/usage-policies)). "To achieve zero data retention, customers must take specific actions or avoid specific features", and grounding with Google Search stores data for 30 days ([ZDR](https://ai.google.dev/gemini-api/docs/zdr)).
- **Vertex AI** (Google Cloud's AI platform, now presented as Gemini Enterprise Agent Platform). "Google won't use your data to train or fine-tune any AI/ML models without your prior permission or instruction" ([data governance](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/data-governance)). The `eu` endpoint "strictly covers data residency within EU member states"; the global endpoint "may be processed in any Google Cloud location around the world" ([data residency](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/data-residency)).

### Microsoft (Azure OpenAI in Microsoft Foundry)

- [Prompts](Glossary.md#prompt) and completions "are NOT available to OpenAI" and "are NOT used to train any generative AI foundation models without your permission or instruction"; data is "processed within the customer-specified geography (unless you are using a Global or DataZone deployment type)" ([data privacy](https://learn.microsoft.com/en-us/azure/ai-foundry/responsible-ai/openai/data-privacy)).
- Customers "who meet additional Limited Access eligibility criteria" can "apply to modify abuse monitoring" ([abuse monitoring](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/abuse-monitoring)).

### Mistral

- Mistral's help pages now call its consumer chat app Vibe. "Input and output data are used by default to train our artificial intelligence models" on Vibe, while "Enterprise customers are opted out of training by default" ([help](https://help.mistral.ai/en/articles/347617-do-you-use-my-user-data-to-train-your-artificial-intelligence-models)). Opt-out toggles for Vibe and the API are separate ([help](https://help.mistral.ai/en/articles/455207-can-i-opt-out-of-my-input-or-output-data-being-used-for-training)).
- API retention: "we keep your Input and Output for the period necessary to generate the Output and then for thirty (30) rolling days to monitor abuse (unless zero data retention is activated)" ([privacy policy](https://legal.mistral.ai/terms/privacy-policy)). ZDR is "available only with pay-as-you-go and only for stateless API calls", and Mistral may "at our discretion, approve or deny it" ([help](https://help.mistral.ai/en/articles/347612-can-i-activate-zero-data-retention-zdr)).
- "By default, your data is hosted in the European Union" ([help](https://help.mistral.ai/en/articles/347629-where-do-you-store-my-data-or-my-organization-s-data)).

### Cohere

- **Training is opt-out.** Cohere's commitments cover "enterprise data of our commercial, paying customers". Once opted out, "prompts and generations will not be used to train Cohere models"; to opt out, go to Settings → Data Controls and "Adjust the toggle to 'Off' to opt out". The change is forward-looking: "Your change in settings will apply to data created after you make that change". The page describes the opt-out and does not explicitly say which way the default is set; treat training as on until the toggle is off ([Enterprise Data Commitments](https://cohere.com/enterprise-data-commitments), checked 2026-11-27).
- **Retention.** Cohere will "automatically delete logged prompts and generations after 30 days", unless it needs them for a legal requirement, a customer contract, or flagged usage. "Deleting your account does not delete prompts or generations" (same page).
- **ZDR.** For approved enterprise customers, "we do not log any prompts or generations"; ZDR is limited to customers "who can make additional commitments", and usage metadata is still received (same page).

### Groq

- **No training.** The Services Agreement §4.2 says Groq is "not permitted to use Inputs or Outputs for training or fine-tuning any AI Model Services or other models" unless the customer explicitly permits or instructs it ([agreement](https://console.groq.com/docs/legal/services-agreement), checked 2026-11-27).
- **Retention.** "By default, Groq does not retain customer data for inference requests." For reliability or abuse investigations, "We may temporarily log inputs and outputs" and keep them "up to 30 days, unless legally required to retain longer" ([Your data in GroqCloud](https://console.groq.com/docs/your-data), checked 2026-11-27).
- **ZDR.** Self-serve for all customers. "When ZDR is enabled, Groq will not retain customer data for system reliability and abuse monitoring", and features that need stored data are disabled (same page).

### xAI

- **No training.** "SpaceXSI never trains on your API inputs or outputs without your explicit permission" ([API security FAQ](https://docs.x.ai/developers/faq/security), checked 2026-11-27). The developer documentation currently brands the company "SpaceXSI"; if a contract matters, confirm the legal entity.
- **Retention.** "all API requests and responses are stored on our servers (encrypted at rest) for 30 days" for abuse auditing, and "it is automatically deleted after 30 days" (same page).
- **ZDR.** Available and team-wide: "If enabled, ZDR is team-wide", prompts and generated tokens are "never persisted to disk", and the 30-day audit retention does not apply. It disables stateful features such as the Files and Batch APIs (same page).

### Meta

- "Meta uses your interactions with AIs to improve AI at Meta" ([Meta help](https://www.meta.com/help/artificial-intelligence/)). In the EU, interactions with Meta AI "will also be used to train and improve our models", with "a link to a form where people can object" ([Meta newsroom](https://about.fb.com/news/2025/04/making-ai-work-harder-for-europeans/)).
- Since December 2025, Meta says it will "use your interactions with AI at Meta to personalize the content and ads you see" ([Meta newsroom](https://about.fb.com/news/2025/10/improving-your-recommendations-apps-ai-meta/)).
- Meta's [generative AI](Glossary.md#generative-ai) privacy pages on facebook.com could not be loaded on 2026-10-28, so retention and location are not covered here.
- Llama [models](Glossary.md#model) are open-weight: if you run them yourself, Meta receives nothing.

### DeepSeek

- The app may "use Inputs and Outputs to provide, maintain, operate, develop or improve the Services", subject to de-identification, and you "can opt out by turning off "Improve the model for everyone"" ([terms of use](https://cdn.deepseek.com/policies/en-US/deepseek-terms-of-use.html)).
- "we directly collect, process and store your Personal Data in People's Republic of China"; data is kept "for as long as you have an account" ([privacy policy](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html)).
- **The API policy is different from what the separate open-platform terms say.** The Open Platform Privacy Policy (effective 2026-11-11) says that, unless there is a separate written agreement, DeepSeek may use inputs and outputs submitted through the Open Platform to develop, train, evaluate and improve its models, algorithms, safety systems and related technology. It describes no self-service API opt-out, says personal information is stored in mainland China, and says network logs are kept at least six months ([Open Platform privacy policy](https://cdn.deepseek.com/policies/zh-CN/deepseek-open-platform-privacy-policy.html), checked 2026-11-27; the English page returned 404 that day). The separate [open platform terms](https://cdn.deepseek.com/policies/en-US/deepseek-open-platform-terms-of-service.html) do not mention training, retention or location.
- DeepSeek's models are also open-weight, and other [providers](Glossary.md#provider) serve them under their own terms.

## Related pages

- [Data protection when you use AI](Data-protection.md)
- [Security for AI apps](Security-for-AI-apps.md)
- [AI providers and models](AI-providers-and-models.md#where-you-can-get-them)

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [Agent](Glossary.md#agent), [API](Glossary.md#api), [Cloud](Glossary.md#cloud), [Generative AI](Glossary.md#generative-ai), [Inference](Glossary.md#inference), [Logs](Glossary.md#logs), [Model](Glossary.md#model), [Open-weight model](Glossary.md#open-weight-model), [Prompt](Glossary.md#prompt), [Provider](Glossary.md#provider), [Zero data retention (ZDR)](Glossary.md#zero-data-retention-zdr).
<!-- SEEALSO:END -->

## Sources

All vendor pages are linked in the table and in the details above. Most were checked on 2026-10-28; the Cohere, Groq, xAI and DeepSeek API sources were checked on 2026-11-27. Pages marked † refused automated access on 2026-10-28. Corrections with a link to the current vendor page are especially welcome.

---

First version written with AI assistance and checked against the vendor pages listed under [sources](#sources) on 2026-10-28. Updated on 2026-11-27 with Cohere, Groq, xAI and the DeepSeek API policy. Not legal advice. Found a mistake or a policy change? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
