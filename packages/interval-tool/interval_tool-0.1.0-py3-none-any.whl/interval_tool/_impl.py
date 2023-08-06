from tail_recursion import tail_recursive, TailRecursion


def drop_short(xss, min_emit_length, start_fn, stop_fn):
    """
    Drop elements that are smaller than min_emit_length in length.
    """
    yss = []
    for xs in xss:
        if len(xs) == 0:
            continue
        else:
            start = start_fn(xs)
            stop = stop_fn(xs)
            length = stop - start
            if length >= min_emit_length:
                yss.append(xs)
    return yss


@tail_recursive
def max_min_merge(xss, max_break, min_emit_length, buf, acc, start_fn, stop_fn):
    if not xss:
        # exhausted, consume the buffer
        if buf is not None:
            acc.append(buf)
        return drop_short(acc, min_emit_length, start_fn, stop_fn)
    else:
        # consume the head
        h = xss[0]
        t = xss[1:]
        if buf is None:
            # put this one to buf and wait for the next
            buf = h
            return TailRecursion(t, max_break, min_emit_length, buf, acc, start_fn, stop_fn)
        else:
            # maybe merge the buf with the current one
            start = stop_fn(buf)
            stop = start_fn(h)
            length = stop - start
            if length > max_break:
                # buf is too far away from this one, consumes the buf and starts anew
                acc.append(buf)
                buf = h
                return TailRecursion(t, max_break, min_emit_length, buf, acc, start_fn, stop_fn)
            else:
                # buf is close enough, merge them two, and continue merging
                buf.extend(h)
                return TailRecursion(t, max_break, min_emit_length, buf, acc, start_fn, stop_fn)


def geq_threshold_and_merge(xs, threshold, max_break, min_emit_length, start_fn, stop_fn, value_fn):
    xss = []
    for x in xs:
        v = value_fn(x)
        if v >= threshold:
            xss.append([x])
    return max_min_merge(xss, max_break, min_emit_length, None, [], start_fn, stop_fn)


def geq_threshold_and_merge_linear_id(xs, threshold, max_break, min_emit_length, w):

    ys = [[i, x] for i, x in enumerate(xs)]

    def start_fn(zs):
        return w * zs[0][0]

    def stop_fn(zs):
        return w * zs[-1][0] + w

    def value_fn(z):
        return z[1]

    return geq_threshold_and_merge(ys, threshold, max_break, min_emit_length, start_fn, stop_fn, value_fn)