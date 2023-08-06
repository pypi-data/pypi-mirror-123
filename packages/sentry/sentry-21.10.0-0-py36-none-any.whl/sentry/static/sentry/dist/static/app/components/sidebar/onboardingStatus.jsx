Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const sidebar_1 = (0, tslib_1.__importDefault)(require("app/components/onboardingWizard/sidebar"));
const taskConfig_1 = require("app/components/onboardingWizard/taskConfig");
const progressRing_1 = (0, tslib_1.__importStar)(require("app/components/progressRing"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const types_1 = require("./types");
const isDone = (task) => task.status === 'complete' || task.status === 'skipped';
const progressTextCss = () => (0, react_2.css) `
  font-size: ${theme_1.default.fontSizeMedium};
  font-weight: bold;
`;
function OnboardingStatus({ collapsed, org, projects, currentPanel, orientation, hidePanel, onShowPanel, }) {
    var _a;
    const handleShowPanel = () => {
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'onboarding.wizard_opened',
            eventName: 'Onboarding Wizard Opened',
            organization_id: org.id,
        });
        onShowPanel();
    };
    if (!((_a = org.features) === null || _a === void 0 ? void 0 : _a.includes('onboarding'))) {
        return null;
    }
    const tasks = (0, taskConfig_1.getMergedTasks)({ organization: org, projects });
    const allDisplayedTasks = tasks.filter(task => task.display);
    const doneTasks = allDisplayedTasks.filter(isDone);
    const numberRemaining = allDisplayedTasks.length - doneTasks.length;
    const pendingCompletionSeen = doneTasks.some(task => allDisplayedTasks.some(displayedTask => displayedTask.task === task.task) &&
        task.status === 'complete' &&
        !task.completionSeen);
    const isActive = currentPanel === types_1.SidebarPanelKey.OnboardingWizard;
    if (doneTasks.length >= allDisplayedTasks.length && !isActive) {
        return null;
    }
    const label = (0, locale_1.t)('Quick Start');
    return (<react_1.Fragment>
      <Container role="button" aria-label={label} onClick={handleShowPanel} isActive={isActive}>
        <progressRing_1.default animateText textCss={progressTextCss} text={allDisplayedTasks.length - doneTasks.length} value={(doneTasks.length / allDisplayedTasks.length) * 100} backgroundColor="rgba(255, 255, 255, 0.15)" progressEndcaps="round" size={38} barWidth={6}/>
        {!collapsed && (<div>
            <Heading>{label}</Heading>
            <Remaining>
              {(0, locale_1.tct)('[numberRemaining] Remaining tasks', { numberRemaining })}
              {pendingCompletionSeen && <PendingSeenIndicator />}
            </Remaining>
          </div>)}
      </Container>
      {isActive && (<sidebar_1.default orientation={orientation} collapsed={collapsed} onClose={hidePanel}/>)}
    </react_1.Fragment>);
}
const Heading = (0, styled_1.default)('div') `
  transition: color 100ms;
  font-size: ${p => p.theme.backgroundSecondary};
  color: ${p => p.theme.gray200};
  margin-bottom: ${(0, space_1.default)(0.25)};
`;
const Remaining = (0, styled_1.default)('div') `
  transition: color 100ms;
  font-size: ${p => p.theme.fontSizeSmall};
  color: ${p => p.theme.gray300};
  display: grid;
  grid-template-columns: max-content max-content;
  grid-gap: ${(0, space_1.default)(0.75)};
  align-items: center;
`;
const PendingSeenIndicator = (0, styled_1.default)('div') `
  background: ${p => p.theme.red300};
  border-radius: 50%;
  height: 7px;
  width: 7px;
`;
const hoverCss = (p) => (0, react_2.css) `
  background: rgba(255, 255, 255, 0.05);

  ${progressRing_1.RingBackground} {
    stroke: rgba(255, 255, 255, 0.3);
  }
  ${progressRing_1.RingBar} {
    stroke: ${p.theme.green200};
  }
  ${progressRing_1.RingText} {
    color: ${p.theme.white};
  }

  ${Heading} {
    color: ${p.theme.white};
  }
  ${Remaining} {
    color: ${p.theme.gray200};
  }
`;
const Container = (0, styled_1.default)('div') `
  padding: 9px 19px 9px 16px;
  cursor: pointer;
  display: grid;
  grid-template-columns: max-content 1fr;
  grid-gap: ${(0, space_1.default)(1.5)};
  align-items: center;
  transition: background 100ms;

  ${p => p.isActive && hoverCss(p)};

  &:hover {
    ${hoverCss};
  }
`;
exports.default = (0, withProjects_1.default)(OnboardingStatus);
//# sourceMappingURL=onboardingStatus.jsx.map