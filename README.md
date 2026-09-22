# Commit Helper

A small, offline Python CLI and library for **composing and validating Conventional Commit messages**. It gives teams a deterministic local check without network access, AI services, or Git hooks being required.

## English

### Why it exists
Consistent commit messages improve changelogs, reviews, release automation, and repository history. Commit Helper focuses on one job: making Conventional Commit headers easy to compose and validate in terminals and CI.

### Features
- Compose `type(scope)!: description` messages safely.
- Validate the standard commit types: `build`, `chore`, `ci`, `docs`, `feat`, `fix`, `perf`, `refactor`, `revert`, `style`, `test`.
- Parse scope, breaking marker, description, body, and footer lines.
- Configurable header length (72 by default).
- Style warnings for capitalized descriptions, trailing periods, and breaking markers without a `BREAKING CHANGE:` footer.
- Strict mode promotes warnings to errors.
- Human-readable or JSON output with CI-friendly exit codes.
- Read messages from an argument, UTF-8 file, or stdin.
- Reusable Python API; no runtime dependencies; no network calls.

### Requirements & installation
Requires Python 3.10+.

```bash
python -m pip install -e .
commit-helper --version
```

For development:

```bash
python -m pip install -e . pytest
pytest -q
```

### Usage
Compose a message:

```bash
commit-helper compose feat "add CSV export" --scope reports
# feat(reports): add CSV export
```

Compose a breaking change with body/footer:

```bash
commit-helper compose feat "replace token format" --scope auth --breaking \
  --body "Consumers must migrate stored tokens." \
  --footer "BREAKING CHANGE: old tokens are no longer accepted"
```

Validate directly, from a file, or stdin:

```bash
commit-helper validate --message "fix(api): handle empty payload"
commit-helper validate --file .git/COMMIT_EDITMSG --strict
printf "docs: update guide" | commit-helper validate --stdin --json
```

Exit codes: `0` valid, `1` validation failure, `2` input/usage error.

### Python API
```python
from commit_helper import compose, validate

message = compose("feat", "add export", scope="reports")
print(message.render())
result = validate(message.render())
assert result.valid
```

### Configuration
There is intentionally no config file. Use `--max-header 72` (20–200) and `--strict` explicitly so CI behavior remains visible and reproducible.

### Project structure
```text
src/commit_helper/   core model, parser, validator, CLI
tests/               core and CLI tests
.github/workflows/   cross-platform CI
pyproject.toml        package and entry-point metadata
```

### Testing & preview
CI runs compilation, pytest, and a CLI smoke test on Python 3.10/3.12/3.13 across Ubuntu, Windows, and macOS. This is a terminal tool, so screenshots are optional; the commands above are the intended preview.

### Security & privacy
Commit Helper is offline. It does not execute Git, run commit contents, modify repositories, send telemetry, or contact external services. Avoid placing secrets in commit messages in the first place. See [SECURITY.md](SECURITY.md).

### Limitations
This implements a practical Conventional Commits subset, not every organization-specific convention. Footer parsing is deliberately lightweight; it preserves footer lines rather than interpreting every Git trailer rule. It does not install Git hooks, generate changelogs, or commit changes for you. Validation cannot determine whether a message accurately describes the code change.

### Optional roadmap
Possible future additions include opt-in project configuration, Git hook templates, and richer Git-trailer parsing. These are not required for current functionality.

### Contributing & license
See [CONTRIBUTING.md](CONTRIBUTING.md). Licensed under the [MIT License](LICENSE).

### Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

## العربية

### نظرة عامة
**Commit Helper** أداة سطر أوامر ومكتبة Python محلية تساعد على إنشاء رسائل **Conventional Commits** والتحقق منها بشكل ثابت وواضح، دون شبكة أو خدمات ذكاء اصطناعي أو اعتماديات تشغيل خارجية.

### لماذا المشروع؟
رسائل الالتزام المتناسقة تجعل سجل المشروع أوضح، وتفيد في مراجعة الكود وإنشاء سجل التغييرات وأتمتة الإصدارات. يركز المشروع على مهمة محددة: صياغة رسالة الالتزام والتحقق من بنيتها محليًا وفي CI.

### الميزات
- إنشاء رسائل بصيغة `type(scope)!: description`.
- التحقق من الأنواع القياسية المدعومة مثل `feat` و`fix` و`docs` و`test` وغيرها.
- تحليل النطاق ووصف التغيير وعلامة التغيير الكاسر والنص والتذييلات.
- حد افتراضي 72 محرفًا لرأس الرسالة مع إمكانية تغييره.
- تحذيرات أسلوبية للوصف الذي يبدأ بحرف إنجليزي كبير أو ينتهي بنقطة، وللتغيير الكاسر بلا تذييل `BREAKING CHANGE:`.
- وضع `--strict` لتحويل التحذيرات إلى أخطاء.
- مخرجات نصية أو JSON ورموز خروج مناسبة للأتمتة.
- القراءة من وسيطة أو ملف UTF-8 أو stdin.
- Python API قابلة لإعادة الاستخدام، بلا اتصال خارجي.

### المتطلبات والتثبيت
يتطلب Python 3.10 أو أحدث:

```bash
python -m pip install -e .
commit-helper --version
```

للتطوير والاختبار:

```bash
python -m pip install -e . pytest
pytest -q
```

### الاستخدام
```bash
commit-helper compose feat "add CSV export" --scope reports
commit-helper validate --message "fix(api): handle empty payload"
commit-helper validate --file .git/COMMIT_EDITMSG --strict
```

رموز الخروج: `0` للرسالة الصحيحة، `1` لفشل التحقق، و`2` لخطأ الإدخال أو القراءة.

### Python API
```python
from commit_helper import compose, validate
message = compose("docs", "update guide")
assert validate(message.render()).valid
```

### الإعداد
لا يوجد ملف إعداد مخفي عمدًا. استخدم `--max-header` و`--strict` صراحةً لكي تبقى قواعد CI واضحة وقابلة لإعادة الإنتاج.

### بنية المشروع
المحرك والـCLI داخل `src/commit_helper/`، والاختبارات داخل `tests/`، وCI داخل `.github/workflows/`، وبيانات الحزمة في `pyproject.toml`.

### الاختبارات والمعاينة
إعداد CI يفحص compilation ويشغل pytest واختبار CLI على Python 3.10 و3.12 و3.13 في Ubuntu وWindows وmacOS. المشروع طرفي، لذلك لا يحتاج واجهة رسومية أو صور شاشة حتى يكون قابلًا للاستخدام.

### الأمان والخصوصية
الأداة محلية بالكامل: لا تشغّل أوامر Git، ولا تنفذ محتوى الرسائل، ولا تعدّل المستودع، ولا ترسل telemetry، ولا تتصل بخدمة خارجية. تجنب أصلًا وضع الأسرار داخل رسائل الالتزام. راجع [SECURITY.md](SECURITY.md).

### القيود
المشروع يطبق مجموعة عملية من Conventional Commits وليس كل قواعد المؤسسات المخصصة. تحليل التذييلات بسيط ويحافظ على السطور دون تفسير جميع قواعد Git trailers. لا يثبت Git hooks ولا ينشئ changelog ولا ينفذ commit نيابةً عن المستخدم، ولا يستطيع التحقق من أن وصف الرسالة يطابق تغيير الكود فعليًا.

### تطوير اختياري
يمكن مستقبلًا إضافة إعدادات مشروع اختيارية، وقوالب Git hooks، وتحليل أعمق للتذييلات، دون أن تكون هذه الإضافات مطلوبة لوظائف الإصدار الحالي.

### المساهمة والترخيص
راجع [CONTRIBUTING.md](CONTRIBUTING.md). المشروع مرخص وفق [MIT](LICENSE).

### المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
