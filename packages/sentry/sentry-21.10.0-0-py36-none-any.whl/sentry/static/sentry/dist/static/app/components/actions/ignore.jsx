Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const modal_1 = require("app/actionCreators/modal");
const actionLink_1 = (0, tslib_1.__importDefault)(require("app/components/actions/actionLink"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const customIgnoreCountModal_1 = (0, tslib_1.__importDefault)(require("app/components/customIgnoreCountModal"));
const customIgnoreDurationModal_1 = (0, tslib_1.__importDefault)(require("app/components/customIgnoreDurationModal"));
const dropdownLink_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownLink"));
const duration_1 = (0, tslib_1.__importDefault)(require("app/components/duration"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("app/types");
const button_1 = (0, tslib_1.__importDefault)(require("./button"));
const menuHeader_1 = (0, tslib_1.__importDefault)(require("./menuHeader"));
const IGNORE_DURATIONS = [30, 120, 360, 60 * 24, 60 * 24 * 7];
const IGNORE_COUNTS = [1, 10, 100, 1000, 10000, 100000];
const IGNORE_WINDOWS = [
    { value: 60, label: (0, locale_1.t)('per hour') },
    { value: 24 * 60, label: (0, locale_1.t)('per day') },
    { value: 24 * 7 * 60, label: (0, locale_1.t)('per week') },
];
const IgnoreActions = ({ onUpdate, disabled, shouldConfirm, confirmMessage, confirmLabel = (0, locale_1.t)('Ignore'), isIgnored = false, }) => {
    const onIgnore = (statusDetails) => {
        return onUpdate({
            status: types_1.ResolutionStatus.IGNORED,
            statusDetails: statusDetails || {},
        });
    };
    const onCustomIgnore = (statusDetails) => {
        onIgnore(statusDetails);
    };
    const actionLinkProps = {
        shouldConfirm,
        title: (0, locale_1.t)('Ignore'),
        message: confirmMessage,
        confirmLabel,
        disabled,
    };
    if (isIgnored) {
        return (<tooltip_1.default title={(0, locale_1.t)('Change status to unresolved')}>
        <button_1.default priority="primary" onClick={() => onUpdate({ status: types_1.ResolutionStatus.UNRESOLVED })} label={(0, locale_1.t)('Unignore')} icon={<icons_1.IconMute size="xs"/>}/>
      </tooltip_1.default>);
    }
    const openCustomIgnoreDuration = () => (0, modal_1.openModal)(deps => (<customIgnoreDurationModal_1.default {...deps} onSelected={details => onCustomIgnore(details)}/>));
    const openCustomIgnoreCount = () => (0, modal_1.openModal)(deps => (<customIgnoreCountModal_1.default {...deps} onSelected={details => onCustomIgnore(details)} label={(0, locale_1.t)('Ignore this issue until it occurs again\u2026')} countLabel={(0, locale_1.t)('Number of times')} countName="ignoreCount" windowName="ignoreWindow" windowOptions={IGNORE_WINDOWS}/>));
    const openCustomIgnoreUserCount = () => (0, modal_1.openModal)(deps => (<customIgnoreCountModal_1.default {...deps} onSelected={details => onCustomIgnore(details)} label={(0, locale_1.t)('Ignore this issue until it affects an additional\u2026')} countLabel={(0, locale_1.t)('Number of users')} countName="ignoreUserCount" windowName="ignoreUserWindow" windowOptions={IGNORE_WINDOWS}/>));
    return (<buttonBar_1.default merged>
      <actionLink_1.default {...actionLinkProps} type="button" title={(0, locale_1.t)('Ignore')} onAction={() => onUpdate({ status: types_1.ResolutionStatus.IGNORED })} icon={<icons_1.IconMute size="xs"/>}>
        {(0, locale_1.t)('Ignore')}
      </actionLink_1.default>
      <StyledDropdownLink customTitle={<button_1.default disabled={disabled} icon={<icons_1.IconChevron direction="down" size="xs"/>}/>} alwaysRenderMenu disabled={disabled}>
        <menuHeader_1.default>{(0, locale_1.t)('Ignore')}</menuHeader_1.default>

        <DropdownMenuItem>
          <dropdownLink_1.default title={<ActionSubMenu>
                {(0, locale_1.t)('For\u2026')}
                <SubMenuChevron>
                  <icons_1.IconChevron direction="right" size="xs"/>
                </SubMenuChevron>
              </ActionSubMenu>} caret={false} isNestedDropdown alwaysRenderMenu>
            {IGNORE_DURATIONS.map(duration => (<DropdownMenuItem key={duration}>
                <StyledForActionLink {...actionLinkProps} onAction={() => onIgnore({ ignoreDuration: duration })}>
                  <ActionSubMenu>
                    <duration_1.default seconds={duration * 60}/>
                  </ActionSubMenu>
                </StyledForActionLink>
              </DropdownMenuItem>))}
            <DropdownMenuItem>
              <ActionSubMenu>
                <a onClick={openCustomIgnoreDuration}>{(0, locale_1.t)('Custom')}</a>
              </ActionSubMenu>
            </DropdownMenuItem>
          </dropdownLink_1.default>
        </DropdownMenuItem>

        <DropdownMenuItem>
          <dropdownLink_1.default title={<ActionSubMenu>
                {(0, locale_1.t)('Until this occurs again\u2026')}
                <SubMenuChevron>
                  <icons_1.IconChevron direction="right" size="xs"/>
                </SubMenuChevron>
              </ActionSubMenu>} caret={false} isNestedDropdown alwaysRenderMenu>
            {IGNORE_COUNTS.map(count => (<DropdownMenuItem key={count}>
                <dropdownLink_1.default title={<ActionSubMenu>
                      {count === 1
                    ? (0, locale_1.t)('one time\u2026') // This is intentional as unbalanced string formatters are problematic
                    : (0, locale_1.tn)('%s time\u2026', '%s times\u2026', count)}
                      <SubMenuChevron>
                        <icons_1.IconChevron direction="right" size="xs"/>
                      </SubMenuChevron>
                    </ActionSubMenu>} caret={false} isNestedDropdown alwaysRenderMenu>
                  <DropdownMenuItem>
                    <StyledActionLink {...actionLinkProps} onAction={() => onIgnore({ ignoreCount: count })}>
                      {(0, locale_1.t)('from now')}
                    </StyledActionLink>
                  </DropdownMenuItem>
                  {IGNORE_WINDOWS.map(({ value, label }) => (<DropdownMenuItem key={value}>
                      <StyledActionLink {...actionLinkProps} onAction={() => onIgnore({
                    ignoreCount: count,
                    ignoreWindow: value,
                })}>
                        {label}
                      </StyledActionLink>
                    </DropdownMenuItem>))}
                </dropdownLink_1.default>
              </DropdownMenuItem>))}
            <DropdownMenuItem>
              <ActionSubMenu>
                <a onClick={openCustomIgnoreCount}>{(0, locale_1.t)('Custom')}</a>
              </ActionSubMenu>
            </DropdownMenuItem>
          </dropdownLink_1.default>
        </DropdownMenuItem>
        <DropdownMenuItem>
          <dropdownLink_1.default title={<ActionSubMenu>
                {(0, locale_1.t)('Until this affects an additional\u2026')}
                <SubMenuChevron>
                  <icons_1.IconChevron direction="right" size="xs"/>
                </SubMenuChevron>
              </ActionSubMenu>} caret={false} isNestedDropdown alwaysRenderMenu>
            {IGNORE_COUNTS.map(count => (<DropdownMenuItem key={count}>
                <dropdownLink_1.default title={<ActionSubMenu>
                      {(0, locale_1.tn)('one user\u2026', '%s users\u2026', count)}
                      <SubMenuChevron>
                        <icons_1.IconChevron direction="right" size="xs"/>
                      </SubMenuChevron>
                    </ActionSubMenu>} caret={false} isNestedDropdown alwaysRenderMenu>
                  <DropdownMenuItem>
                    <StyledActionLink {...actionLinkProps} onAction={() => onIgnore({ ignoreUserCount: count })}>
                      {(0, locale_1.t)('from now')}
                    </StyledActionLink>
                  </DropdownMenuItem>
                  {IGNORE_WINDOWS.map(({ value, label }) => (<DropdownMenuItem key={value}>
                      <StyledActionLink {...actionLinkProps} onAction={() => onIgnore({
                    ignoreUserCount: count,
                    ignoreUserWindow: value,
                })}>
                        {label}
                      </StyledActionLink>
                    </DropdownMenuItem>))}
                </dropdownLink_1.default>
              </DropdownMenuItem>))}
            <DropdownMenuItem>
              <ActionSubMenu>
                <a onClick={openCustomIgnoreUserCount}>{(0, locale_1.t)('Custom')}</a>
              </ActionSubMenu>
            </DropdownMenuItem>
          </dropdownLink_1.default>
        </DropdownMenuItem>
      </StyledDropdownLink>
    </buttonBar_1.default>);
};
exports.default = IgnoreActions;
const actionLinkCss = p => (0, react_1.css) `
  color: ${p.theme.subText};
  &:hover {
    border-radius: ${p.theme.borderRadius};
    background: ${p.theme.bodyBackground} !important;
  }
`;
const StyledActionLink = (0, styled_1.default)(actionLink_1.default) `
  padding: 7px 10px !important;
  ${actionLinkCss};
`;
const StyledForActionLink = (0, styled_1.default)(actionLink_1.default) `
  padding: ${(0, space_1.default)(0.5)} 0;
  ${actionLinkCss};
`;
const StyledDropdownLink = (0, styled_1.default)(dropdownLink_1.default) `
  transition: none;
  border-top-left-radius: 0 !important;
  border-bottom-left-radius: 0 !important;
`;
const DropdownMenuItem = (0, styled_1.default)('li') `
  :not(:last-child) {
    border-bottom: 1px solid ${p => p.theme.innerBorder};
  }
  > span {
    display: block;
    > ul {
      border-radius: ${p => p.theme.borderRadius};
      top: 5px;
      left: 100%;
      margin-top: -5px;
      margin-left: -1px;
      &:after,
      &:before {
        display: none !important;
      }
    }
  }
  &:hover > span {
    background: ${p => p.theme.focus};
  }
`;
const ActionSubMenu = (0, styled_1.default)('span') `
  display: grid;
  grid-template-columns: 200px 1fr;
  grid-column-start: 1;
  grid-column-end: 4;
  gap: ${(0, space_1.default)(1)};
  padding: ${(0, space_1.default)(0.5)} 0;
  color: ${p => p.theme.textColor};
  a {
    color: ${p => p.theme.textColor};
  }
`;
const SubMenuChevron = (0, styled_1.default)('span') `
  display: grid;
  align-self: center;
  color: ${p => p.theme.gray300};
  transition: 0.1s color linear;

  &:hover,
  &:active {
    color: ${p => p.theme.subText};
  }
`;
//# sourceMappingURL=ignore.jsx.map