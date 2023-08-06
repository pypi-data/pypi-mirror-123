Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_dom_1 = (0, tslib_1.__importDefault)(require("react-dom"));
const react_popper_1 = require("react-popper");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const menuHeader_1 = (0, tslib_1.__importDefault)(require("app/components/actions/menuHeader"));
const checkboxFancy_1 = (0, tslib_1.__importDefault)(require("app/components/checkboxFancy/checkboxFancy"));
const menuItem_1 = (0, tslib_1.__importDefault)(require("app/components/menuItem"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const constants_1 = require("app/utils/performance/constants");
class TeamKeyTransaction extends react_1.Component {
    constructor(props) {
        super(props);
        this.state = {
            isOpen: false,
        };
        this.handleClickOutside = (event) => {
            if (!this.menuEl) {
                return;
            }
            if (!(event.target instanceof Element)) {
                return;
            }
            if (this.menuEl.contains(event.target)) {
                return;
            }
            this.setState({ isOpen: false });
        };
        this.toggleOpen = () => {
            this.setState(({ isOpen }) => ({ isOpen: !isOpen }));
        };
        this.toggleSelection = (enabled, selection) => () => {
            const { handleToggleKeyTransaction } = this.props;
            return enabled ? handleToggleKeyTransaction(selection) : undefined;
        };
        let portal = document.getElementById('team-key-transaction-portal');
        if (!portal) {
            portal = document.createElement('div');
            portal.setAttribute('id', 'team-key-transaction-portal');
            document.body.appendChild(portal);
        }
        this.portalEl = portal;
        this.menuEl = null;
    }
    componentDidUpdate(_props, prevState) {
        if (this.state.isOpen && prevState.isOpen === false) {
            document.addEventListener('click', this.handleClickOutside, true);
        }
        if (this.state.isOpen === false && prevState.isOpen) {
            document.removeEventListener('click', this.handleClickOutside, true);
        }
    }
    componentWillUnmount() {
        document.removeEventListener('click', this.handleClickOutside, true);
        this.portalEl.remove();
    }
    partitionTeams(counts, keyedTeams) {
        var _a;
        const { teams, project } = this.props;
        const enabledTeams = [];
        const disabledTeams = [];
        const noAccessTeams = [];
        const projectTeams = new Set(project.teams.map(({ id }) => id));
        for (const team of teams) {
            if (!projectTeams.has(team.id)) {
                noAccessTeams.push(team);
            }
            else if (keyedTeams.has(team.id) ||
                ((_a = counts.get(team.id)) !== null && _a !== void 0 ? _a : 0) < constants_1.MAX_TEAM_KEY_TRANSACTIONS) {
                enabledTeams.push(team);
            }
            else {
                disabledTeams.push(team);
            }
        }
        return {
            enabledTeams,
            disabledTeams,
            noAccessTeams,
        };
    }
    renderMenuContent(counts, keyedTeams) {
        const { teams, project, transactionName } = this.props;
        const { enabledTeams, disabledTeams, noAccessTeams } = this.partitionTeams(counts, keyedTeams);
        const isMyTeamsEnabled = enabledTeams.length > 0;
        const myTeamsHandler = this.toggleSelection(isMyTeamsEnabled, {
            action: enabledTeams.length === keyedTeams.size ? 'unkey' : 'key',
            teamIds: enabledTeams.map(({ id }) => id),
            project,
            transactionName,
        });
        const hasTeamsWithAccess = enabledTeams.length + disabledTeams.length > 0;
        return (<DropdownContent>
        {hasTeamsWithAccess && (<react_1.Fragment>
            <DropdownMenuHeader first>
              {(0, locale_1.t)('My Teams with Access')}
              <ActionItem>
                <checkboxFancy_1.default isDisabled={!isMyTeamsEnabled} isChecked={teams.length === keyedTeams.size} isIndeterminate={teams.length > keyedTeams.size && keyedTeams.size > 0} onClick={myTeamsHandler}/>
              </ActionItem>
            </DropdownMenuHeader>
            {enabledTeams.map(team => (<TeamKeyTransactionItem key={team.slug} team={team} isKeyed={keyedTeams.has(team.id)} disabled={false} onSelect={this.toggleSelection(true, {
                        action: keyedTeams.has(team.id) ? 'unkey' : 'key',
                        teamIds: [team.id],
                        project,
                        transactionName,
                    })}/>))}
            {disabledTeams.map(team => (<TeamKeyTransactionItem key={team.slug} team={team} isKeyed={keyedTeams.has(team.id)} disabled onSelect={this.toggleSelection(true, {
                        action: keyedTeams.has(team.id) ? 'unkey' : 'key',
                        teamIds: [team.id],
                        project,
                        transactionName,
                    })}/>))}
          </react_1.Fragment>)}
        {noAccessTeams.length > 0 && (<react_1.Fragment>
            <DropdownMenuHeader first={!hasTeamsWithAccess}>
              {(0, locale_1.t)('My Teams without Access')}
            </DropdownMenuHeader>
            {noAccessTeams.map(team => (<TeamKeyTransactionItem key={team.slug} team={team} disabled/>))}
          </react_1.Fragment>)}
      </DropdownContent>);
    }
    renderMenu() {
        const { isLoading, counts, keyedTeams } = this.props;
        if (isLoading || !(0, utils_1.defined)(counts) || !(0, utils_1.defined)(keyedTeams)) {
            return null;
        }
        const modifiers = {
            hide: {
                enabled: false,
            },
            preventOverflow: {
                padding: 10,
                enabled: true,
                boundariesElement: 'viewport',
            },
        };
        return react_dom_1.default.createPortal(<react_popper_1.Popper placement="top" modifiers={modifiers}>
        {({ ref: popperRef, style, placement }) => (<DropdownWrapper ref={ref => {
                    popperRef(ref);
                    this.menuEl = ref;
                }} style={style} data-placement={placement}>
            {this.renderMenuContent(counts, keyedTeams)}
          </DropdownWrapper>)}
      </react_popper_1.Popper>, this.portalEl);
    }
    render() {
        const { isLoading, error, title: Title, keyedTeams, initialValue, teams } = this.props;
        const { isOpen } = this.state;
        const menu = isOpen ? this.renderMenu() : null;
        return (<react_popper_1.Manager>
        <react_popper_1.Reference>
          {({ ref }) => (<div ref={ref}>
              <Title isOpen={isOpen} disabled={isLoading || Boolean(error)} keyedTeams={keyedTeams ? teams.filter(({ id }) => keyedTeams.has(id)) : null} initialValue={initialValue} onClick={this.toggleOpen}/>
            </div>)}
        </react_popper_1.Reference>
        {menu}
      </react_popper_1.Manager>);
    }
}
function TeamKeyTransactionItem({ team, isKeyed, disabled, onSelect }) {
    return (<DropdownMenuItem key={team.slug} disabled={disabled} onSelect={onSelect} stopPropagation>
      <MenuItemContent>
        {team.slug}
        <ActionItem>
          {!(0, utils_1.defined)(isKeyed) ? null : disabled ? ((0, locale_1.t)('Max %s', constants_1.MAX_TEAM_KEY_TRANSACTIONS)) : (<checkboxFancy_1.default isChecked={isKeyed}/>)}
        </ActionItem>
      </MenuItemContent>
    </DropdownMenuItem>);
}
const DropdownWrapper = (0, styled_1.default)('div') `
  /* Adapted from the dropdown-menu class */
  border: none;
  border-radius: 2px;
  box-shadow: 0 0 0 1px rgba(52, 60, 69, 0.2), 0 1px 3px rgba(70, 82, 98, 0.25);
  background-clip: padding-box;
  background-color: ${p => p.theme.background};
  width: 220px;
  overflow: visible;
  z-index: ${p => p.theme.zIndex.tooltip};

  &:before,
  &:after {
    width: 0;
    height: 0;
    content: '';
    display: block;
    position: absolute;
    right: auto;
  }

  &:before {
    border-left: 9px solid transparent;
    border-right: 9px solid transparent;
    left: calc(50% - 9px);
    z-index: -2;
  }

  &:after {
    border-left: 8px solid transparent;
    border-right: 8px solid transparent;
    left: calc(50% - 8px);
    z-index: -1;
  }

  &[data-placement*='bottom'] {
    margin-top: 9px;

    &:before {
      border-bottom: 9px solid ${p => p.theme.border};
      top: -9px;
    }

    &:after {
      border-bottom: 8px solid ${p => p.theme.background};
      top: -8px;
    }
  }

  &[data-placement*='top'] {
    margin-bottom: 9px;

    &:before {
      border-top: 9px solid ${p => p.theme.border};
      bottom: -9px;
    }

    &:after {
      border-top: 8px solid ${p => p.theme.background};
      bottom: -8px;
    }
  }
`;
const DropdownContent = (0, styled_1.default)('div') `
  max-height: 250px;
  overflow-y: auto;
`;
const DropdownMenuHeader = (0, styled_1.default)(menuHeader_1.default) `
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};

  background: ${p => p.theme.backgroundSecondary};
  ${p => p.first && 'border-radius: 2px'};
`;
const DropdownMenuItem = (0, styled_1.default)(menuItem_1.default) `
  font-size: ${p => p.theme.fontSizeMedium};

  &:not(:last-child) {
    border-bottom: 1px solid ${p => p.theme.innerBorder};
  }
`;
const MenuItemContent = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width: 100%;
`;
const ActionItem = (0, styled_1.default)('span') `
  min-width: ${(0, space_1.default)(2)};
  margin-left: ${(0, space_1.default)(1)};
`;
exports.default = TeamKeyTransaction;
//# sourceMappingURL=teamKeyTransaction.jsx.map