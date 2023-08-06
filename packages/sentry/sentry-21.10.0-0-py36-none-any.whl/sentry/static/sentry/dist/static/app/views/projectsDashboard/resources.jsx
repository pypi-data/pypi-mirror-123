Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const breadcrumbs_generic_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/breadcrumbs-generic.svg"));
const code_arguments_tags_mirrored_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/code-arguments-tags-mirrored.svg"));
const releases_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/releases.svg"));
const pageHeading_1 = (0, tslib_1.__importDefault)(require("app/components/pageHeading"));
const resourceCard_1 = (0, tslib_1.__importDefault)(require("app/components/resourceCard"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
function Resources({ organization }) {
    (0, react_1.useEffect)(() => {
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'orgdash.resources_shown',
            eventName: 'Projects Dashboard: Resources Shown',
            organization_id: organization.id,
        });
    }, []);
    return (<ResourcesWrapper data-test-id="resources">
      <pageHeading_1.default withMargins>{(0, locale_1.t)('Resources')}</pageHeading_1.default>
      <ResourceCards>
        <resourceCard_1.default link="https://blog.sentry.io/2018/03/06/the-sentry-workflow" imgUrl={releases_svg_1.default} title={(0, locale_1.t)('The Sentry Workflow')}/>
        <resourceCard_1.default link="https://sentry.io/vs/logging/" imgUrl={breadcrumbs_generic_svg_1.default} title={(0, locale_1.t)('Sentry vs Logging')}/>
        <resourceCard_1.default link="https://docs.sentry.io/" imgUrl={code_arguments_tags_mirrored_svg_1.default} title={(0, locale_1.t)('Docs')}/>
      </ResourceCards>
    </ResourcesWrapper>);
}
exports.default = Resources;
const ResourcesWrapper = (0, styled_1.default)('div') `
  border-top: 1px solid ${p => p.theme.border};
  padding: 25px 30px 10px 30px;
`;
const ResourceCards = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: minmax(100px, 1fr);
  grid-gap: ${(0, space_1.default)(3)};

  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  }
`;
//# sourceMappingURL=resources.jsx.map