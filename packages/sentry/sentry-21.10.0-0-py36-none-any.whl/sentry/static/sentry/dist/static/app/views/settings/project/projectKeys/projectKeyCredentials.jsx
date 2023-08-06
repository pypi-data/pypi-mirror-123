Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const textCopyInput_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/textCopyInput"));
const DEFAULT_PROPS = {
    showDsn: true,
    showDsnPublic: true,
    showSecurityEndpoint: true,
    showMinidump: true,
    showUnreal: true,
    showPublicKey: false,
    showSecretKey: false,
    showProjectId: false,
};
class ProjectKeyCredentials extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            showDeprecatedDsn: false,
        };
        this.toggleDeprecatedDsn = () => {
            this.setState(state => ({
                showDeprecatedDsn: !state.showDeprecatedDsn,
            }));
        };
    }
    render() {
        const { showDeprecatedDsn } = this.state;
        const { projectId, data, showDsn, showDsnPublic, showSecurityEndpoint, showMinidump, showUnreal, showPublicKey, showSecretKey, showProjectId, } = this.props;
        return (<react_1.Fragment>
        {showDsnPublic && (<field_1.default label={(0, locale_1.t)('DSN')} inline={false} flexibleControlStateSize help={(0, locale_1.tct)('The DSN tells the SDK where to send the events to. [link]', {
                    link: showDsn ? (<link_1.default to="" onClick={this.toggleDeprecatedDsn}>
                  {showDeprecatedDsn
                            ? (0, locale_1.t)('Hide deprecated DSN')
                            : (0, locale_1.t)('Show deprecated DSN')}
                </link_1.default>) : null,
                })}>
            <textCopyInput_1.default>
              {(0, getDynamicText_1.default)({
                    value: data.dsn.public,
                    fixed: '__DSN__',
                })}
            </textCopyInput_1.default>
            {showDeprecatedDsn && (<StyledField label={null} help={(0, locale_1.t)('Deprecated DSN includes a secret which is no longer required by newer SDK versions. If you are unsure which to use, follow installation instructions for your language.')} inline={false} flexibleControlStateSize>
                <textCopyInput_1.default>
                  {(0, getDynamicText_1.default)({
                        value: data.dsn.secret,
                        fixed: '__DSN_DEPRECATED__',
                    })}
                </textCopyInput_1.default>
              </StyledField>)}
          </field_1.default>)}

        {/* this edge case should imho not happen, but just to be sure */}
        {!showDsnPublic && showDsn && (<field_1.default label={(0, locale_1.t)('DSN (Deprecated)')} help={(0, locale_1.t)('Deprecated DSN includes a secret which is no longer required by newer SDK versions. If you are unsure which to use, follow installation instructions for your language.')} inline={false} flexibleControlStateSize>
            <textCopyInput_1.default>
              {(0, getDynamicText_1.default)({
                    value: data.dsn.secret,
                    fixed: '__DSN_DEPRECATED__',
                })}
            </textCopyInput_1.default>
          </field_1.default>)}

        {showSecurityEndpoint && (<field_1.default label={(0, locale_1.t)('Security Header Endpoint')} help={(0, locale_1.t)('Use your security header endpoint for features like CSP and Expect-CT reports.')} inline={false} flexibleControlStateSize>
            <textCopyInput_1.default>
              {(0, getDynamicText_1.default)({
                    value: data.dsn.security,
                    fixed: '__SECURITY_HEADER_ENDPOINT__',
                })}
            </textCopyInput_1.default>
          </field_1.default>)}

        {showMinidump && (<field_1.default label={(0, locale_1.t)('Minidump Endpoint')} help={(0, locale_1.tct)('Use this endpoint to upload [link], for example with Electron, Crashpad or Breakpad.', {
                    link: (<externalLink_1.default href="https://docs.sentry.io/platforms/native/guides/minidumps/">
                    minidump crash reports
                  </externalLink_1.default>),
                })} inline={false} flexibleControlStateSize>
            <textCopyInput_1.default>
              {(0, getDynamicText_1.default)({
                    value: data.dsn.minidump,
                    fixed: '__MINIDUMP_ENDPOINT__',
                })}
            </textCopyInput_1.default>
          </field_1.default>)}

        {showUnreal && (<field_1.default label={(0, locale_1.t)('Unreal Engine 4 Endpoint')} help={(0, locale_1.t)('Use this endpoint to configure your UE4 Crash Reporter.')} inline={false} flexibleControlStateSize>
            <textCopyInput_1.default>
              {(0, getDynamicText_1.default)({
                    value: data.dsn.unreal || '',
                    fixed: '__UNREAL_ENDPOINT__',
                })}
            </textCopyInput_1.default>
          </field_1.default>)}

        {showPublicKey && (<field_1.default label={(0, locale_1.t)('Public Key')} inline flexibleControlStateSize>
            <textCopyInput_1.default>
              {(0, getDynamicText_1.default)({
                    value: data.public,
                    fixed: '__PUBLICKEY__',
                })}
            </textCopyInput_1.default>
          </field_1.default>)}

        {showSecretKey && (<field_1.default label={(0, locale_1.t)('Secret Key')} inline flexibleControlStateSize>
            <textCopyInput_1.default>
              {(0, getDynamicText_1.default)({
                    value: data.secret,
                    fixed: '__SECRETKEY__',
                })}
            </textCopyInput_1.default>
          </field_1.default>)}

        {showProjectId && (<field_1.default label={(0, locale_1.t)('Project ID')} inline flexibleControlStateSize>
            <textCopyInput_1.default>
              {(0, getDynamicText_1.default)({
                    value: projectId,
                    fixed: '__PROJECTID__',
                })}
            </textCopyInput_1.default>
          </field_1.default>)}
      </react_1.Fragment>);
    }
}
ProjectKeyCredentials.defaultProps = DEFAULT_PROPS;
const StyledField = (0, styled_1.default)(field_1.default) `
  padding: ${(0, space_1.default)(0.5)} 0 0 0;
`;
exports.default = ProjectKeyCredentials;
//# sourceMappingURL=projectKeyCredentials.jsx.map