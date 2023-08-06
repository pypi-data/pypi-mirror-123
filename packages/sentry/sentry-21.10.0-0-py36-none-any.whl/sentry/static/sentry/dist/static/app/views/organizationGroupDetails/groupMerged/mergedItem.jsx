Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const groupingActions_1 = (0, tslib_1.__importDefault)(require("app/actions/groupingActions"));
const checkbox_1 = (0, tslib_1.__importDefault)(require("app/components/checkbox"));
const eventOrGroupHeader_1 = (0, tslib_1.__importDefault)(require("app/components/eventOrGroupHeader"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const groupingStore_1 = (0, tslib_1.__importDefault)(require("app/stores/groupingStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
class MergedItem extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            collapsed: false,
            checked: false,
            busy: false,
        };
        this.listener = groupingStore_1.default.listen(data => this.onGroupChange(data), undefined);
        this.onGroupChange = ({ unmergeState }) => {
            if (!unmergeState) {
                return;
            }
            const { fingerprint } = this.props;
            const stateForId = unmergeState.has(fingerprint.id)
                ? unmergeState.get(fingerprint.id)
                : undefined;
            if (!stateForId) {
                return;
            }
            Object.keys(stateForId).forEach(key => {
                if (stateForId[key] === this.state[key]) {
                    return;
                }
                this.setState(prevState => (Object.assign(Object.assign({}, prevState), { [key]: stateForId[key] })));
            });
        };
        this.handleToggleEvents = () => {
            const { fingerprint } = this.props;
            groupingActions_1.default.toggleCollapseFingerprint(fingerprint.id);
        };
        this.handleToggle = () => {
            const { fingerprint } = this.props;
            const { latestEvent } = fingerprint;
            if (this.state.busy) {
                return;
            }
            // clicking anywhere in the row will toggle the checkbox
            groupingActions_1.default.toggleUnmerge([fingerprint.id, latestEvent.id]);
        };
    }
    // Disable default behavior of toggling checkbox
    handleLabelClick(event) {
        event.preventDefault();
    }
    handleCheckClick() {
        // noop because of react warning about being a controlled input without `onChange`
        // we handle change via row click
    }
    renderFingerprint(id, label) {
        if (!label) {
            return id;
        }
        return (<tooltip_1.default title={id}>
        <code>{label}</code>
      </tooltip_1.default>);
    }
    render() {
        const { fingerprint, organization } = this.props;
        const { latestEvent, id, label } = fingerprint;
        const { collapsed, busy, checked } = this.state;
        const checkboxDisabled = busy;
        // `latestEvent` can be null if last event w/ fingerprint is not within retention period
        return (<MergedGroup busy={busy}>
        <Controls expanded={!collapsed}>
          <ActionWrapper onClick={this.handleToggle}>
            <checkbox_1.default id={id} value={id} checked={checked} disabled={checkboxDisabled} onChange={this.handleCheckClick}/>

            <FingerprintLabel onClick={this.handleLabelClick} htmlFor={id}>
              {this.renderFingerprint(id, label)}
            </FingerprintLabel>
          </ActionWrapper>

          <div>
            <Collapse onClick={this.handleToggleEvents}>
              <icons_1.IconChevron direction={collapsed ? 'down' : 'up'} size="xs"/>
            </Collapse>
          </div>
        </Controls>

        {!collapsed && (<MergedEventList className="event-list">
            {latestEvent && (<EventDetails className="event-details">
                <eventOrGroupHeader_1.default data={latestEvent} organization={organization} hideIcons hideLevel/>
              </EventDetails>)}
          </MergedEventList>)}
      </MergedGroup>);
    }
}
const MergedGroup = (0, styled_1.default)('div') `
  ${p => p.busy && 'opacity: 0.2'};
`;
const ActionWrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-auto-flow: column;
  align-items: center;
  gap: ${(0, space_1.default)(1)};

  /* Can't use styled components for this because of broad selector */
  input[type='checkbox'] {
    margin: 0;
  }
`;
const Controls = (0, styled_1.default)('div') `
  display: flex;
  justify-content: space-between;
  border-top: 1px solid ${p => p.theme.innerBorder};
  background-color: ${p => p.theme.backgroundSecondary};
  padding: ${(0, space_1.default)(0.5)} ${(0, space_1.default)(1)};
  ${p => p.expanded && `border-bottom: 1px solid ${p.theme.innerBorder}`};

  ${MergedGroup} {
    &:first-child & {
      border-top: none;
    }
    &:last-child & {
      border-top: none;
      border-bottom: 1px solid ${p => p.theme.innerBorder};
    }
  }
`;
const FingerprintLabel = (0, styled_1.default)('label') `
  font-family: ${p => p.theme.text.familyMono};

  ${ /* sc-selector */Controls} & {
    font-weight: 400;
    margin: 0;
  }
`;
const Collapse = (0, styled_1.default)('span') `
  cursor: pointer;
`;
const MergedEventList = (0, styled_1.default)('div') `
  overflow: hidden;
  border: none;
  background-color: ${p => p.theme.background};
`;
const EventDetails = (0, styled_1.default)('div') `
  display: flex;
  justify-content: space-between;

  .event-list & {
    padding: ${(0, space_1.default)(1)};
  }
`;
exports.default = MergedItem;
//# sourceMappingURL=mergedItem.jsx.map