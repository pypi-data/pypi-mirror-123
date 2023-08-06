Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const indicator_1 = require("app/actionCreators/indicator");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const locale_1 = require("app/locale");
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
class AdminMail extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.sendTestEmail = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const testMailEmail = this.state.data.testMailEmail;
            try {
                yield this.api.requestPromise('/internal/mail/', { method: 'POST' });
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('A test email has been sent to %s', testMailEmail));
            }
            catch (error) {
                (0, indicator_1.addErrorMessage)(error.responseJSON
                    ? error.responseJSON.error
                    : (0, locale_1.t)('Unable to send test email. Check your server logs'));
            }
        });
    }
    getEndpoints() {
        return [['data', '/internal/mail/']];
    }
    renderBody() {
        const { data } = this.state;
        const { mailHost, mailPassword, mailUsername, mailPort, mailUseTls, mailUseSsl, mailFrom, mailListNamespace, testMailEmail, } = data;
        return (<div>
        <h3>{(0, locale_1.t)('SMTP Settings')}</h3>

        <dl className="vars">
          <dt>{(0, locale_1.t)('From Address')}</dt>
          <dd>
            <pre className="val">{mailFrom}</pre>
          </dd>

          <dt>{(0, locale_1.t)('Host')}</dt>
          <dd>
            <pre className="val">
              {mailHost}:{mailPort}
            </pre>
          </dd>

          <dt>{(0, locale_1.t)('Username')}</dt>
          <dd>
            <pre className="val">{mailUsername || <em>{(0, locale_1.t)('not set')}</em>}</pre>
          </dd>

          <dt>{(0, locale_1.t)('Password')}</dt>
          <dd>
            <pre className="val">
              {mailPassword ? '********' : <em>{(0, locale_1.t)('not set')}</em>}
            </pre>
          </dd>

          <dt>{(0, locale_1.t)('STARTTLS?')}</dt>
          <dd>
            <pre className="val">{mailUseTls ? (0, locale_1.t)('Yes') : (0, locale_1.t)('No')}</pre>
          </dd>

          <dt>{(0, locale_1.t)('SSL?')}</dt>
          <dd>
            <pre className="val">{mailUseSsl ? (0, locale_1.t)('Yes') : (0, locale_1.t)('No')}</pre>
          </dd>

          <dt>{(0, locale_1.t)('Mailing List Namespace')}</dt>
          <dd>
            <pre className="val">{mailListNamespace}</pre>
          </dd>
        </dl>

        <h3>{(0, locale_1.t)('Test Settings')}</h3>

        <p>
          {(0, locale_1.t)("Send an email to your account's email address to confirm that everything is configured correctly.")}
        </p>

        <button_1.default onClick={this.sendTestEmail}>
          {(0, locale_1.t)('Send a test email to %s', testMailEmail)}
        </button_1.default>
      </div>);
    }
}
exports.default = AdminMail;
//# sourceMappingURL=adminMail.jsx.map