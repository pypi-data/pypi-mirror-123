Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const role_1 = (0, tslib_1.__importDefault)(require("app/components/acl/role"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const fileSize_1 = (0, tslib_1.__importDefault)(require("app/components/fileSize"));
const tag_1 = (0, tslib_1.__importDefault)(require("app/components/tag"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const SourceMapsArtifactRow = ({ artifact, onDelete, downloadUrl, downloadRole, }) => {
    const { name, size, dateCreated, id, dist } = artifact;
    const handleDeleteClick = () => {
        onDelete(id);
    };
    return (<react_1.Fragment>
      <NameColumn>
        <Name>{name || `(${(0, locale_1.t)('empty')})`}</Name>
        <TimeAndDistWrapper>
          <TimeWrapper>
            <icons_1.IconClock size="sm"/>
            <timeSince_1.default date={dateCreated}/>
          </TimeWrapper>
          <StyledTag type={dist ? 'info' : undefined} tooltipText={dist ? undefined : (0, locale_1.t)('No distribution set')}>
            {dist !== null && dist !== void 0 ? dist : (0, locale_1.t)('none')}
          </StyledTag>
        </TimeAndDistWrapper>
      </NameColumn>
      <SizeColumn>
        <fileSize_1.default bytes={size}/>
      </SizeColumn>
      <ActionsColumn>
        <buttonBar_1.default gap={0.5}>
          <role_1.default role={downloadRole}>
            {({ hasRole }) => (<tooltip_1.default title={(0, locale_1.t)('You do not have permission to download artifacts.')} disabled={hasRole}>
                <button_1.default size="small" icon={<icons_1.IconDownload size="sm"/>} disabled={!hasRole} href={downloadUrl} title={hasRole ? (0, locale_1.t)('Download Artifact') : undefined}/>
              </tooltip_1.default>)}
          </role_1.default>

          <access_1.default access={['project:releases']}>
            {({ hasAccess }) => (<tooltip_1.default disabled={hasAccess} title={(0, locale_1.t)('You do not have permission to delete artifacts.')}>
                <confirm_1.default message={(0, locale_1.t)('Are you sure you want to remove this artifact?')} onConfirm={handleDeleteClick} disabled={!hasAccess}>
                  <button_1.default size="small" icon={<icons_1.IconDelete size="sm"/>} title={hasAccess ? (0, locale_1.t)('Remove Artifact') : undefined} label={(0, locale_1.t)('Remove Artifact')} disabled={!hasAccess}/>
                </confirm_1.default>
              </tooltip_1.default>)}
          </access_1.default>
        </buttonBar_1.default>
      </ActionsColumn>
    </react_1.Fragment>);
};
const NameColumn = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
`;
const SizeColumn = (0, styled_1.default)('div') `
  display: flex;
  justify-content: flex-end;
  text-align: right;
  align-items: center;
`;
const ActionsColumn = (0, styled_1.default)(SizeColumn) ``;
const Name = (0, styled_1.default)('div') `
  padding-right: ${(0, space_1.default)(4)};
  overflow-wrap: break-word;
  word-break: break-all;
`;
const TimeAndDistWrapper = (0, styled_1.default)('div') `
  width: 100%;
  display: flex;
  margin-top: ${(0, space_1.default)(1)};
  align-items: center;
`;
const TimeWrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(0.5)};
  grid-template-columns: min-content 1fr;
  font-size: ${p => p.theme.fontSizeMedium};
  align-items: center;
  color: ${p => p.theme.subText};
`;
const StyledTag = (0, styled_1.default)(tag_1.default) `
  margin-left: ${(0, space_1.default)(1)};
`;
exports.default = SourceMapsArtifactRow;
//# sourceMappingURL=sourceMapsArtifactRow.jsx.map