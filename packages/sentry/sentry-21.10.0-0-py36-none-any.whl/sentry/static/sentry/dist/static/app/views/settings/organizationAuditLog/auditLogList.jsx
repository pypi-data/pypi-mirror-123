Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const userAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/userAvatar"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const selectField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectField"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const avatarStyle = {
    width: 36,
    height: 36,
    marginRight: 8,
};
const AuditLogList = ({ pageLinks, entries, eventType, eventTypes, onEventSelect, }) => {
    const hasEntries = entries && entries.length > 0;
    const ipv4Length = 15;
    const options = [
        { value: '', label: (0, locale_1.t)('Any action'), clearableVaue: false },
        ...eventTypes.map(type => ({ label: type, value: type, clearableValue: false })),
    ];
    const action = (<form>
      <selectField_1.default name="event" onChange={onEventSelect} value={eventType} style={{ width: 250 }} options={options}/>
    </form>);
    return (<div>
      <settingsPageHeader_1.default title={(0, locale_1.t)('Audit Log')} action={action}/>
      <panels_1.Panel>
        <StyledPanelHeader disablePadding>
          <div>{(0, locale_1.t)('Member')}</div>
          <div>{(0, locale_1.t)('Action')}</div>
          <div>{(0, locale_1.t)('IP')}</div>
          <div>{(0, locale_1.t)('Time')}</div>
        </StyledPanelHeader>

        <panels_1.PanelBody>
          {!hasEntries && <emptyMessage_1.default>{(0, locale_1.t)('No audit entries available')}</emptyMessage_1.default>}

          {hasEntries &&
            entries.map(entry => (<StyledPanelItem center key={entry.id}>
                <UserInfo>
                  <div>
                    {entry.actor.email && (<userAvatar_1.default style={avatarStyle} user={entry.actor}/>)}
                  </div>
                  <NameContainer>
                    <Name data-test-id="actor-name">
                      {entry.actor.isSuperuser
                    ? (0, locale_1.t)('%s (Sentry Staff)', entry.actor.name)
                    : entry.actor.name}
                    </Name>
                    <Note>{entry.note}</Note>
                  </NameContainer>
                </UserInfo>
                <div>
                  <MonoDetail>{entry.event}</MonoDetail>
                </div>
                <TimestampOverflow>
                  <tooltip_1.default title={entry.ipAddress} disabled={entry.ipAddress && entry.ipAddress.length <= ipv4Length}>
                    <MonoDetail>{entry.ipAddress}</MonoDetail>
                  </tooltip_1.default>
                </TimestampOverflow>
                <TimestampInfo>
                  <dateTime_1.default dateOnly date={entry.dateCreated}/>
                  <dateTime_1.default timeOnly format="LT zz" date={entry.dateCreated}/>
                </TimestampInfo>
              </StyledPanelItem>))}
        </panels_1.PanelBody>
      </panels_1.Panel>
      {pageLinks && <pagination_1.default pageLinks={pageLinks}/>}
    </div>);
};
const UserInfo = (0, styled_1.default)('div') `
  display: flex;
  line-height: 1.2;
  font-size: 13px;
  flex: 1;
`;
const NameContainer = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
  justify-content: center;
`;
const Name = (0, styled_1.default)('div') `
  font-weight: 600;
  font-size: 15px;
`;
const Note = (0, styled_1.default)('div') `
  font-size: 13px;
  word-break: break-word;
`;
const TimestampOverflow = (0, styled_1.default)('div') `
  ${overflowEllipsis_1.default};
`;
const MonoDetail = (0, styled_1.default)('code') `
  font-size: ${p => p.theme.fontSizeMedium};
`;
const StyledPanelHeader = (0, styled_1.default)(panels_1.PanelHeader) `
  display: grid;
  grid-template-columns: 1fr max-content 130px 150px;
  grid-column-gap: ${(0, space_1.default)(2)};
  padding: ${(0, space_1.default)(2)};
`;
const StyledPanelItem = (0, styled_1.default)(panels_1.PanelItem) `
  display: grid;
  grid-template-columns: 1fr max-content 130px 150px;
  grid-column-gap: ${(0, space_1.default)(2)};
  padding: ${(0, space_1.default)(2)};
`;
const TimestampInfo = (0, styled_1.default)('div') `
  display: grid;
  grid-template-rows: auto auto;
  grid-gap: ${(0, space_1.default)(1)};
  font-size: ${p => p.theme.fontSizeMedium};
`;
exports.default = AuditLogList;
//# sourceMappingURL=auditLogList.jsx.map