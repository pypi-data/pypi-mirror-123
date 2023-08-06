Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const count_1 = (0, tslib_1.__importDefault)(require("app/components/count"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const version_1 = (0, tslib_1.__importDefault)(require("app/components/version"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const SourceMapsArchiveRow = ({ archive, orgId, projectId, onDelete }) => {
    const { name, date, fileCount } = archive;
    const archiveLink = `/settings/${orgId}/projects/${projectId}/source-maps/${encodeURIComponent(name)}`;
    return (<react_1.Fragment>
      <Column>
        <textOverflow_1.default>
          <link_1.default to={archiveLink}>
            <version_1.default version={name} anchor={false} tooltipRawVersion truncate/>
          </link_1.default>
        </textOverflow_1.default>
      </Column>
      <ArtifactsColumn>
        <count_1.default value={fileCount}/>
      </ArtifactsColumn>
      <Column>{(0, locale_1.t)('release')}</Column>
      <Column>
        <dateTime_1.default date={date}/>
      </Column>
      <ActionsColumn>
        <buttonBar_1.default gap={0.5}>
          <access_1.default access={['project:releases']}>
            {({ hasAccess }) => (<tooltip_1.default disabled={hasAccess} title={(0, locale_1.t)('You do not have permission to delete artifacts.')}>
                <confirm_1.default onConfirm={() => onDelete(name)} message={(0, locale_1.t)('Are you sure you want to remove all artifacts in this archive?')} disabled={!hasAccess}>
                  <button_1.default size="small" icon={<icons_1.IconDelete size="sm"/>} title={(0, locale_1.t)('Remove All Artifacts')} label={(0, locale_1.t)('Remove All Artifacts')} disabled={!hasAccess}/>
                </confirm_1.default>
              </tooltip_1.default>)}
          </access_1.default>
        </buttonBar_1.default>
      </ActionsColumn>
    </react_1.Fragment>);
};
const Column = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  overflow: hidden;
`;
const ArtifactsColumn = (0, styled_1.default)(Column) `
  padding-right: ${(0, space_1.default)(4)};
  text-align: right;
  justify-content: flex-end;
`;
const ActionsColumn = (0, styled_1.default)(Column) `
  justify-content: flex-end;
`;
exports.default = SourceMapsArchiveRow;
//# sourceMappingURL=sourceMapsArchiveRow.jsx.map