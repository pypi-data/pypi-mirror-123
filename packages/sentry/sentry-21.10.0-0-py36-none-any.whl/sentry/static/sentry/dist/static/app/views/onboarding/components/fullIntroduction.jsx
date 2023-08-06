Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const framer_motion_1 = require("framer-motion");
const modal_1 = require("app/actionCreators/modal");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const platforms_1 = (0, tslib_1.__importDefault)(require("app/data/platforms"));
const locale_1 = require("app/locale");
const setupIntroduction_1 = (0, tslib_1.__importDefault)(require("./setupIntroduction"));
function FullIntroduction({ currentPlatform }) {
    var _a, _b;
    return (<React.Fragment>
      <setupIntroduction_1.default stepHeaderText={(0, locale_1.t)('Prepare the %s SDK', (_b = (_a = platforms_1.default.find(p => p.id === currentPlatform)) === null || _a === void 0 ? void 0 : _a.name) !== null && _b !== void 0 ? _b : '')} platform={currentPlatform}/>
      <framer_motion_1.motion.p variants={{
            initial: { opacity: 0 },
            animate: { opacity: 1 },
            exit: { opacity: 0 },
        }}>
        {(0, locale_1.tct)("Don't have a relationship with your terminal? [link:Invite your team instead].", {
            link: (<button_1.default priority="link" data-test-id="onboarding-getting-started-invite-members" onClick={() => {
                    (0, modal_1.openInviteMembersModal)();
                }}/>),
        })}
      </framer_motion_1.motion.p>
    </React.Fragment>);
}
exports.default = FullIntroduction;
//# sourceMappingURL=fullIntroduction.jsx.map