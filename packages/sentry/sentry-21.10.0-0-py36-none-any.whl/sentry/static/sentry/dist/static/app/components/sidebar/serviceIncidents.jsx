Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const serviceIncidents_1 = require("app/actionCreators/serviceIncidents");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const list_1 = (0, tslib_1.__importDefault)(require("../list"));
const listItem_1 = (0, tslib_1.__importDefault)(require("../list/listItem"));
const sidebarItem_1 = (0, tslib_1.__importDefault)(require("./sidebarItem"));
const sidebarPanel_1 = (0, tslib_1.__importDefault)(require("./sidebarPanel"));
const sidebarPanelEmpty_1 = (0, tslib_1.__importDefault)(require("./sidebarPanelEmpty"));
const sidebarPanelItem_1 = (0, tslib_1.__importDefault)(require("./sidebarPanelItem"));
class ServiceIncidents extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            status: null,
        };
    }
    componentDidMount() {
        this.fetchData();
    }
    fetchData() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            try {
                const status = yield (0, serviceIncidents_1.loadIncidents)();
                this.setState({ status });
            }
            catch (e) {
                Sentry.withScope(scope => {
                    scope.setLevel(Sentry.Severity.Warning);
                    scope.setFingerprint(['ServiceIncidents-fetchData']);
                    Sentry.captureException(e);
                });
            }
        });
    }
    render() {
        const { currentPanel, onShowPanel, hidePanel, collapsed, orientation } = this.props;
        const { status } = this.state;
        if (!status) {
            return null;
        }
        const active = currentPanel === 'statusupdate';
        const isEmpty = !status.incidents || status.incidents.length === 0;
        if (isEmpty) {
            return null;
        }
        return (<react_1.Fragment>
        <sidebarItem_1.default id="statusupdate" orientation={orientation} collapsed={collapsed} active={active} icon={<icons_1.IconWarning size="md"/>} label={(0, locale_1.t)('Service status')} onClick={onShowPanel}/>
        {active && status && (<sidebarPanel_1.default orientation={orientation} title={(0, locale_1.t)('Recent service updates')} hidePanel={hidePanel} collapsed={collapsed}>
            {isEmpty && (<sidebarPanelEmpty_1.default>
                {(0, locale_1.t)('There are no incidents to report')}
              </sidebarPanelEmpty_1.default>)}
            <IncidentList className="incident-list">
              {status.incidents.map(incident => (<sidebarPanelItem_1.default title={incident.name} message={(0, locale_1.t)('Latest updates')} key={incident.id}>
                  {incident.updates ? (<list_1.default>
                      {incident.updates.map((update, key) => (<listItem_1.default key={key}>{update}</listItem_1.default>))}
                    </list_1.default>) : null}
                  <ActionBar>
                    <button_1.default href={incident.url} size="small" external>
                      {(0, locale_1.t)('Learn more')}
                    </button_1.default>
                  </ActionBar>
                </sidebarPanelItem_1.default>))}
            </IncidentList>
          </sidebarPanel_1.default>)}
      </react_1.Fragment>);
    }
}
exports.default = ServiceIncidents;
const IncidentList = (0, styled_1.default)('div') ``;
const ActionBar = (0, styled_1.default)('div') `
  margin-top: ${(0, space_1.default)(2)};
`;
//# sourceMappingURL=serviceIncidents.jsx.map