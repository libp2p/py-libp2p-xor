import matplotlib.pyplot as plt
import matplotlib.lines as mlines

from .model import *


def plot(model: LookupModel):
    fig, ax = plt.subplots(1)
    plot_lookup(ax, model)
    plt.show()


def plot_lookup(ax, m: LookupModel):
    # plot vertical grid lines on event stamps
    for e in m.events:
        v_line = mlines.Line2D(
            [m.stamp_to_x(e.stamp_ns), m.stamp_to_x(e.stamp_ns)],
            [0, 1.0],
            color='#d0d0d0')
        ax.add_line(v_line)

    # plot horizontal grid lines on peers that were used
    for u in m.used:
        h_line = mlines.Line2D(
            [m.stamp_to_x(m.start_ns), m.stamp_to_x(m.stop_ns)],
            [m.key_to_y(u), m.key_to_y(u)],
            color='#d0d0d0')
        ax.add_line(h_line)

    # plot state changes
    x, y, s, c = [], [], [], []

    def push(e_, k_, c_):
        ex, ey = m.event_key_xy(e_, k_)
        x.append(ex)
        y.append(ey)
        c.append(c_)
        s.append(5.0)

    for e in m.events:
        for k in e.heard():
            push(e, k, '#a0d0a0')  # green
        for k in e.waiting():
            push(e, k, '#000000')   # black
        for k in e.queried():
            push(e, k, '#50c050')  # black
        for k in e.unreachable():
            push(e, k, '#d0a0a0')  # red
        ax.scatter(x, y, s=s, c=c, alpha=0.7, zorder=5, marker='s')

    # plot queries
    for q in m.queries:
        q_line = mlines.Line2D(
            [
                m.stamp_to_x(q.request.stamp_ns),
                m.stamp_to_x(q.response.stamp_ns) if q.response else m.max_x(),
            ],
            [m.key_to_y(q.peer), m.key_to_y(q.peer)],
            linestyle="--",
            linewidth=2.0,
            marker="D",
            color=color_for_query_outcome(q))
        ax.add_line(q_line)

    # plot lookup path
    for q in m.find_path():
        q_line = mlines.Line2D(
            [m.stamp_to_x(q.request.stamp_ns), m.stamp_to_x(q.response.stamp_ns)],
            [m.key_to_y(q.peer), m.key_to_y(q.peer)],
            linestyle="-",
            linewidth=2.0,
            marker="D",
            color='#50c050')
        ax.add_line(q_line)

    # customize axes
    set_xticks_for_model(ax, m)
    set_yticks_for_model(ax, m)
    style_axis(ax)
    ax.set_title("lookup {}".format(m.id))


def color_for_query_outcome(q):
    if q.outcome == QUERY_SUCCESS:
        return '#50c050'  # green
    elif q.outcome == QUERY_UNREACHABLE:
        return '#c05050'  # red
    else:
        return '#5050c0'  # blue


def set_xticks_for_model(ax, m: LookupModel):
    ax.set_xticks([m.stamp_to_x(e.stamp_ns) for e in m.events])
    ax.set_xticklabels([m.stamp_to_x(e.stamp_ns) for e in m.events], rotation='vertical')
    # span = m.max_x() - m.min_x()
    # ax.set_xlim([m.min_x() - 0.1 * span, m.max_x() + 0.1 * span])
    ax.set_xlim([m.min_x(), m.max_x()])


def set_yticks_for_model(ax, m: LookupModel):
    ax.set_yticks([m.key_to_y(u) for u in m.used])
    ax.set_yticklabels([m.key_to_y(u) for u in m.used])
    # span = m.max_y() - m.min_y()
    # ax.set_ylim([m.min_y() - 0.1 * span, m.max_y() + 0.1 * span])
    ax.set_ylim([m.min_y(), m.max_y()])


def style_axis(ax):
    # ax.grid(zorder=0)
    ax.grid(False)
    ax.tick_params(axis='both', which='major', labelsize=6)
    ax.tick_params(axis='both', which='minor', labelsize=6)
