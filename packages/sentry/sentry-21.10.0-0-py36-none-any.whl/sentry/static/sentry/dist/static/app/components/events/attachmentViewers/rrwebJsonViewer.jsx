Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const jsonViewer_1 = (0, tslib_1.__importDefault)(require("app/components/events/attachmentViewers/jsonViewer"));
const panelAlert_1 = (0, tslib_1.__importDefault)(require("app/components/panels/panelAlert"));
const locale_1 = require("app/locale");
class RRWebJsonViewer extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            showRawJson: false,
        };
    }
    render() {
        const { showRawJson } = this.state;
        return (<react_1.Fragment>
        <StyledPanelAlert border={showRawJson} type="info">
          {(0, locale_1.tct)('This is an attachment containing a session replay. [replayLink:View the replay] or [jsonLink:view the raw JSON].', {
                replayLink: <a href="#context-replay"/>,
                jsonLink: (<a onClick={() => this.setState(state => ({
                        showRawJson: !state.showRawJson,
                    }))}/>),
            })}
        </StyledPanelAlert>
        {showRawJson && <jsonViewer_1.default {...this.props}/>}
      </react_1.Fragment>);
    }
}
exports.default = RRWebJsonViewer;
const StyledPanelAlert = (0, styled_1.default)(panelAlert_1.default) `
  margin: 0;
  border-bottom: ${p => (p.border ? `1px solid ${p.theme.border}` : null)};
`;
//# sourceMappingURL=rrwebJsonViewer.jsx.map