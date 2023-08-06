Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const teamAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/teamAvatar"));
const userAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/userAvatar"));
const memberListStore_1 = (0, tslib_1.__importDefault)(require("app/stores/memberListStore"));
const teamStore_1 = (0, tslib_1.__importDefault)(require("app/stores/teamStore"));
class ActorAvatar extends React.Component {
    render() {
        var _a;
        const _b = this.props, { actor } = _b, props = (0, tslib_1.__rest)(_b, ["actor"]);
        if (actor.type === 'user') {
            const user = actor.id ? (_a = memberListStore_1.default.getById(actor.id)) !== null && _a !== void 0 ? _a : actor : actor;
            return <userAvatar_1.default user={user} {...props}/>;
        }
        if (actor.type === 'team') {
            const team = teamStore_1.default.getById(actor.id);
            return <teamAvatar_1.default team={team} {...props}/>;
        }
        Sentry.withScope(scope => {
            scope.setExtra('actor', actor);
            Sentry.captureException(new Error('Unknown avatar type'));
        });
        return null;
    }
}
ActorAvatar.defaultProps = {
    size: 24,
    hasTooltip: true,
};
exports.default = ActorAvatar;
//# sourceMappingURL=actorAvatar.jsx.map