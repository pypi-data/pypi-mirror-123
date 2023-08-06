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
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("./utils");
const DebugFileRow = ({ debugFile, showDetails, downloadUrl, downloadRole, onDelete, }) => {
    const { id, data, debugId, uuid, size, dateCreated, objectName, cpuName, symbolType, codeId, } = debugFile;
    const fileType = (0, utils_1.getFileType)(debugFile);
    const { features } = data || {};
    return (<react_1.Fragment>
      <Column>
        <div>
          <DebugId>{debugId || uuid}</DebugId>
        </div>
        <TimeAndSizeWrapper>
          <StyledFileSize bytes={size}/>
          <TimeWrapper>
            <icons_1.IconClock size="xs"/>
            <timeSince_1.default date={dateCreated}/>
          </TimeWrapper>
        </TimeAndSizeWrapper>
      </Column>
      <Column>
        <Name>
          {symbolType === 'proguard' && objectName === 'proguard-mapping'
            ? '\u2015'
            : objectName}
        </Name>
        <Description>
          <DescriptionText>
            {symbolType === 'proguard' && cpuName === 'any'
            ? (0, locale_1.t)('proguard mapping')
            : `${cpuName} (${symbolType}${fileType ? ` ${fileType}` : ''})`}
          </DescriptionText>

          {features && (<FeatureTags>
              {features.map(feature => (<StyledTag key={feature} tooltipText={(0, utils_1.getFeatureTooltip)(feature)}>
                  {feature}
                </StyledTag>))}
            </FeatureTags>)}
          {showDetails && (<div>
              {/* there will be more stuff here in the future */}
              {codeId && (<DetailsItem>
                  {(0, locale_1.t)('Code ID')}: {codeId}
                </DetailsItem>)}
            </div>)}
        </Description>
      </Column>
      <RightColumn>
        <buttonBar_1.default gap={0.5}>
          <role_1.default role={downloadRole}>
            {({ hasRole }) => (<tooltip_1.default disabled={hasRole} title={(0, locale_1.t)('You do not have permission to download debug files.')}>
                <button_1.default size="xsmall" icon={<icons_1.IconDownload size="xs"/>} href={downloadUrl} disabled={!hasRole}>
                  {(0, locale_1.t)('Download')}
                </button_1.default>
              </tooltip_1.default>)}
          </role_1.default>
          <access_1.default access={['project:write']}>
            {({ hasAccess }) => (<tooltip_1.default disabled={hasAccess} title={(0, locale_1.t)('You do not have permission to delete debug files.')}>
                <confirm_1.default confirmText={(0, locale_1.t)('Delete')} message={(0, locale_1.t)('Are you sure you wish to delete this file?')} onConfirm={() => onDelete(id)} disabled={!hasAccess}>
                  <button_1.default priority="danger" icon={<icons_1.IconDelete size="xs"/>} size="xsmall" disabled={!hasAccess} data-test-id="delete-dif"/>
                </confirm_1.default>
              </tooltip_1.default>)}
          </access_1.default>
        </buttonBar_1.default>
      </RightColumn>
    </react_1.Fragment>);
};
const DescriptionText = (0, styled_1.default)('span') `
  display: inline-flex;
  margin: 0 ${(0, space_1.default)(1)} ${(0, space_1.default)(1)} 0;
`;
const FeatureTags = (0, styled_1.default)('div') `
  display: inline-flex;
  flex-wrap: wrap;
  margin: -${(0, space_1.default)(0.5)};
`;
const StyledTag = (0, styled_1.default)(tag_1.default) `
  padding: ${(0, space_1.default)(0.5)};
`;
const Column = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
  align-items: flex-start;
`;
const RightColumn = (0, styled_1.default)('div') `
  display: flex;
  justify-content: flex-end;
  align-items: flex-start;
  margin-top: ${(0, space_1.default)(1)};
`;
const DebugId = (0, styled_1.default)('code') `
  font-size: ${p => p.theme.fontSizeSmall};
`;
const TimeAndSizeWrapper = (0, styled_1.default)('div') `
  width: 100%;
  display: flex;
  font-size: ${p => p.theme.fontSizeSmall};
  margin-top: ${(0, space_1.default)(1)};
  color: ${p => p.theme.subText};
  align-items: center;
`;
const StyledFileSize = (0, styled_1.default)(fileSize_1.default) `
  flex: 1;
  padding-left: ${(0, space_1.default)(0.5)};
`;
const TimeWrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(0.5)};
  grid-template-columns: min-content 1fr;
  flex: 2;
  align-items: center;
  padding-left: ${(0, space_1.default)(0.5)};
`;
const Name = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeMedium};
  margin-bottom: ${(0, space_1.default)(1)};
`;
const Description = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeSmall};
  color: ${p => p.theme.subText};
  @media (max-width: ${p => p.theme.breakpoints[2]}) {
    line-height: 1.7;
  }
`;
const DetailsItem = (0, styled_1.default)('div') `
  ${overflowEllipsis_1.default}
  margin-top: ${(0, space_1.default)(1)}
`;
exports.default = DebugFileRow;
//# sourceMappingURL=debugFileRow.jsx.map