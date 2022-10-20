import numpy as np
import gameplay.baseTasks
import gameplay.tasks.check
import gameplay.tasks.moveDownNorth
import gameplay.tasks.moveDownSouth
import gameplay.tasks.moveUpNorth
import gameplay.tasks.moveUpSouth
import gameplay.tasks.useRope
import gameplay.tasks.useShovel


def resolveTasksByWaypointType(context, waypoint):
    if waypoint['type'] == 'check':
        tasks = gameplay.tasks.check.makeCheckTasks(waypoint)
        return tasks
    elif waypoint['type'] == 'floor':
        tasks = gameplay.baseTasks.makeWalkpointTasks(
            context, waypoint['coordinate'])
        return tasks
    elif waypoint['type'] == 'moveDownNorth':
        tasks = gameplay.tasks.moveDownNorth.makeMoveDownNorthTasks(
            context, context['waypoints']['state']['goalCoordinate'], waypoint['coordinate'])
        return tasks
    elif waypoint['type'] == 'moveDownSouth':
        tasks = gameplay.tasks.moveDownSouth.makeMoveDownSouthTasks(
            context, context['waypoints']['state']['goalCoordinate'], waypoint['coordinate'])
        return tasks
    elif waypoint['type'] == 'moveUpNorth':
        tasks = gameplay.tasks.moveUpNorth.makeMoveUpNorthTasks(
            context, context['waypoints']['state']['goalCoordinate'], waypoint['coordinate'])
        return tasks
    elif waypoint['type'] == 'moveUpSouth':
        tasks = gameplay.tasks.moveUpSouth.makeMoveUpSouthTasks(
            context, context['waypoints']['state']['goalCoordinate'], waypoint['coordinate'])
        return tasks
    elif waypoint['type'] == 'useRope':
        tasks = gameplay.tasks.useRope.makeUseRopeTasks(
            context, context['waypoints']['state']['goalCoordinate'], waypoint)
        for task in tasks:
            context['tasks'] = np.append(context['tasks'], [task])
        return tasks
    elif waypoint['type'] == 'useShovel':
        tasks = gameplay.tasks.useShovel.makeUseShovelTasks(
            context, context['waypoints']['state']['goalCoordinate'], waypoint)
        for task in tasks:
            context['tasks'] = np.append(context['tasks'], [task])
        return tasks
