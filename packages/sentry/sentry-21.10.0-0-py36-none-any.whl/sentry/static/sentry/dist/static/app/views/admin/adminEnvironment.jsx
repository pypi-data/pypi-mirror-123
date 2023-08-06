Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
class AdminEnvironment extends asyncView_1.default {
    getEndpoints() {
        return [['data', '/internal/environment/']];
    }
    renderBody() {
        const { data } = this.state;
        const { environment, config, pythonVersion } = data;
        const { version } = configStore_1.default.getConfig();
        return (<div>
        <h3>{(0, locale_1.t)('Environment')}</h3>

        {environment ? (<dl className="vars">
            <VersionLabel>
              {(0, locale_1.t)('Server Version')}
              {version.upgradeAvailable && (<button_1.default title={(0, locale_1.t)("You're running an old version of Sentry, did you know %s is available?", version.latest)} priority="link" href="https://github.com/getsentry/sentry/releases" icon={<icons_1.IconQuestion size="sm"/>} size="small" external/>)}
            </VersionLabel>
            <dd>
              <pre className="val">{version.current}</pre>
            </dd>

            <dt>{(0, locale_1.t)('Python Version')}</dt>
            <dd>
              <pre className="val">{pythonVersion}</pre>
            </dd>
            <dt>{(0, locale_1.t)('Configuration File')}</dt>
            <dd>
              <pre className="val">{environment.config}</pre>
            </dd>
            <dt>{(0, locale_1.t)('Uptime')}</dt>
            <dd>
              <pre className="val">
                {(0, moment_1.default)(environment.start_date).toNow(true)} (since{' '}
                {environment.start_date})
              </pre>
            </dd>
          </dl>) : (<p>
            {(0, locale_1.t)('Environment not found (are you using the builtin Sentry webserver?).')}
          </p>)}

        <h3>
          {(0, locale_1.tct)('Configuration [configPath]', {
                configPath: environment.config && <small>{environment.config}</small>,
            })}
        </h3>

        <dl className="vars">
          {config.map(([key, value]) => (<react_1.Fragment key={key}>
              <dt>{key}</dt>
              <dd>
                <pre className="val">{value}</pre>
              </dd>
            </react_1.Fragment>))}
        </dl>
      </div>);
    }
}
exports.default = AdminEnvironment;
const VersionLabel = (0, styled_1.default)('dt') `
  display: inline-grid;
  grid-auto-flow: column;
  grid-gap: ${(0, space_1.default)(1)};
  align-items: center;
`;
//# sourceMappingURL=adminEnvironment.jsx.map