Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const listLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/listLink"));
const navTabs_1 = (0, tslib_1.__importDefault)(require("app/components/navTabs"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const recreateRoute_1 = (0, tslib_1.__importDefault)(require("app/utils/recreateRoute"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const sessionRow_1 = (0, tslib_1.__importDefault)(require("./sessionRow"));
const utils_1 = require("./utils");
class SessionHistory extends asyncView_1.default {
    getTitle() {
        return (0, locale_1.t)('Session History');
    }
    getEndpoints() {
        return [['ipList', '/users/me/ips/']];
    }
    renderBody() {
        const { ipList } = this.state;
        if (!ipList) {
            return null;
        }
        const { routes, params, location } = this.props;
        const recreateRouteProps = { routes, params, location };
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Security')} tabs={<navTabs_1.default underlined>
              <listLink_1.default to={(0, recreateRoute_1.default)('', Object.assign(Object.assign({}, recreateRouteProps), { stepBack: -1 }))} index>
                {(0, locale_1.t)('Settings')}
              </listLink_1.default>
              <listLink_1.default to={(0, recreateRoute_1.default)('', recreateRouteProps)}>
                {(0, locale_1.t)('Session History')}
              </listLink_1.default>
            </navTabs_1.default>}/>

        <panels_1.Panel>
          <SessionPanelHeader>
            <div>{(0, locale_1.t)('Sessions')}</div>
            <div>{(0, locale_1.t)('First Seen')}</div>
            <div>{(0, locale_1.t)('Last Seen')}</div>
          </SessionPanelHeader>

          <panels_1.PanelBody>
            {ipList.map((_a) => {
                var { id } = _a, ipObj = (0, tslib_1.__rest)(_a, ["id"]);
                return (<sessionRow_1.default key={id} {...ipObj}/>);
            })}
          </panels_1.PanelBody>
        </panels_1.Panel>
      </react_1.Fragment>);
    }
}
exports.default = SessionHistory;
const SessionPanelHeader = (0, styled_1.default)(panels_1.PanelHeader) `
  ${utils_1.tableLayout}
  justify-content: initial;
`;
//# sourceMappingURL=index.jsx.map