Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const congrats_robots_placeholder_jpg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/congrats-robots-placeholder.jpg"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const Placeholder = () => (<PlaceholderImage alt={(0, locale_1.t)('Congrats, you have no unresolved issues')} src={congrats_robots_placeholder_jpg_1.default}/>);
const Message = () => (<React.Fragment>
    <EmptyMessage>
      {(0, locale_1.t)("We couldn't find any issues that matched your filters.")}
    </EmptyMessage>
    <p>{(0, locale_1.t)('Get out there and write some broken code!')}</p>
  </React.Fragment>);
const CongratsRobotsVideo = React.lazy(() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('./congratsRobots'))));
/**
 * Error boundary for loading the robots video.
 * This can error because of the file size of the video
 *
 * Silently ignore the error, this isn't really important enough to
 * capture in Sentry
 */
class ErrorBoundary extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            hasError: false,
        };
    }
    static getDerivedStateFromError() {
        return {
            hasError: true,
        };
    }
    render() {
        if (this.state.hasError) {
            return <Placeholder />;
        }
        return this.props.children;
    }
}
const NoUnresolvedIssues = () => (<Wrapper>
    <ErrorBoundary>
      <React.Suspense fallback={<Placeholder />}>
        <CongratsRobotsVideo />
      </React.Suspense>
    </ErrorBoundary>
    <Message />
  </Wrapper>);
const Wrapper = (0, styled_1.default)('div') `
  display: flex;
  padding: ${(0, space_1.default)(4)} ${(0, space_1.default)(4)};
  flex-direction: column;
  align-items: center;
  text-align: center;
  color: ${p => p.theme.subText};

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    font-size: ${p => p.theme.fontSizeMedium};
  }
`;
const EmptyMessage = (0, styled_1.default)('div') `
  font-weight: 600;

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    font-size: ${p => p.theme.fontSizeExtraLarge};
  }
`;
const PlaceholderImage = (0, styled_1.default)('img') `
  max-height: 320px; /* This should be same height as video in CongratsRobots */
`;
exports.default = NoUnresolvedIssues;
//# sourceMappingURL=noUnresolvedIssues.jsx.map