Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const ROUTE_PREFIX = '/settings/account/api/';
class Row extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: false,
        };
        this.handleRemove = () => {
            if (this.state.loading) {
                return;
            }
            const { api, app, onRemove } = this.props;
            this.setState({
                loading: true,
            }, () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                (0, indicator_1.addLoadingMessage)();
                try {
                    yield api.requestPromise(`/api-applications/${app.id}/`, {
                        method: 'DELETE',
                    });
                    (0, indicator_1.clearIndicators)();
                    onRemove(app);
                }
                catch (_err) {
                    (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to remove application. Please try again.'));
                }
            }));
        };
    }
    render() {
        const { app } = this.props;
        return (<StyledPanelItem>
        <ApplicationNameWrapper>
          <ApplicationName to={`${ROUTE_PREFIX}applications/${app.id}/`}>
            {(0, getDynamicText_1.default)({ value: app.name, fixed: 'CI_APPLICATION_NAME' })}
          </ApplicationName>
          <ClientId>
            {(0, getDynamicText_1.default)({ value: app.clientID, fixed: 'CI_CLIENT_ID' })}
          </ClientId>
        </ApplicationNameWrapper>

        <button_1.default aria-label="Remove" onClick={this.handleRemove} disabled={this.state.loading} icon={<icons_1.IconDelete />}/>
      </StyledPanelItem>);
    }
}
const StyledPanelItem = (0, styled_1.default)(panels_1.PanelItem) `
  padding: ${(0, space_1.default)(2)};
  align-items: center;
`;
const ApplicationNameWrapper = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
  flex: 1;
  margin-right: ${(0, space_1.default)(1)};
`;
const ApplicationName = (0, styled_1.default)(link_1.default) `
  font-size: ${p => p.theme.headerFontSize};
  font-weight: bold;
  margin-bottom: ${(0, space_1.default)(0.5)};
`;
const ClientId = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray200};
  font-size: ${p => p.theme.fontSizeMedium};
`;
exports.default = Row;
//# sourceMappingURL=row.jsx.map