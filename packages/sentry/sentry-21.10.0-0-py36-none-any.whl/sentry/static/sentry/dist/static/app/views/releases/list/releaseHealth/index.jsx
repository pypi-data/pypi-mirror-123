Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const partition_1 = (0, tslib_1.__importDefault)(require("lodash/partition"));
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const content_1 = (0, tslib_1.__importDefault)(require("./content"));
class ReleaseHealth extends react_1.Component {
    shouldComponentUpdate(nextProps) {
        // we don't want project health rows to reorder/jump while the whole card is loading
        if (this.props.reloading && nextProps.reloading) {
            return false;
        }
        return true;
    }
    render() {
        const { release, organization, activeDisplay, location, showPlaceholders, selection, isTopRelease, getHealthData, showReleaseAdoptionStages, } = this.props;
        // sort health rows inside release card alphabetically by project name,
        // show only the ones that are selected in global header
        const [projectsToShow, projectsToHide] = (0, partition_1.default)(release.projects.sort((a, b) => a.slug.localeCompare(b.slug)), p => 
        // do not filter for My Projects & All Projects
        selection.projects.length > 0 && !selection.projects.includes(-1)
            ? selection.projects.includes(p.id)
            : true);
        function getHiddenProjectsTooltip() {
            const limitedProjects = projectsToHide.map(p => p.slug).slice(0, 5);
            const remainderLength = projectsToHide.length - limitedProjects.length;
            if (remainderLength) {
                limitedProjects.push((0, locale_1.tn)('and %s more', 'and %s more', remainderLength));
            }
            return limitedProjects.join(', ');
        }
        return (<react_1.Fragment>
        <content_1.default organization={organization} activeDisplay={activeDisplay} releaseVersion={release.version} showReleaseAdoptionStages={showReleaseAdoptionStages} adoptionStages={release.adoptionStages} projects={projectsToShow} location={location} showPlaceholders={showPlaceholders} isTopRelease={isTopRelease} getHealthData={getHealthData}/>

        {projectsToHide.length > 0 && (<HiddenProjectsMessage>
            <tooltip_1.default title={getHiddenProjectsTooltip()}>
              <textOverflow_1.default>
                {projectsToHide.length === 1
                    ? (0, locale_1.tct)('[number:1] hidden project', { number: <strong /> })
                    : (0, locale_1.tct)('[number] hidden projects', {
                        number: <strong>{projectsToHide.length}</strong>,
                    })}
              </textOverflow_1.default>
            </tooltip_1.default>
          </HiddenProjectsMessage>)}
      </react_1.Fragment>);
    }
}
const HiddenProjectsMessage = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  font-size: ${p => p.theme.fontSizeSmall};
  padding: 0 ${(0, space_1.default)(2)};
  border-top: 1px solid ${p => p.theme.border};
  overflow: hidden;
  height: 24px;
  line-height: 24px;
  color: ${p => p.theme.gray300};
  background-color: ${p => p.theme.backgroundSecondary};
  border-bottom-right-radius: ${p => p.theme.borderRadius};
  @media (max-width: ${p => p.theme.breakpoints[1]}) {
    border-bottom-left-radius: ${p => p.theme.borderRadius};
  }
`;
exports.default = ReleaseHealth;
//# sourceMappingURL=index.jsx.map