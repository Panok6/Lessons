import math


class Link:
    def __init__(self, v1, v2, dist=1):
        if not isinstance(v1, Vertex) or not isinstance(v2, Vertex):
            raise ValueError("Ссылки должны быть обьектами Vertex")
        if v1 == v2:
            raise ValueError("Ссылки должны быть разными")
        self._v1 = v1
        self._v2 = v2
        self._dist = dist
        v1.links = self
        v2.links = self

    @property
    def v1(self):
        return self._v1

    @v1.setter
    def v1(self, val):
        if not isinstance(val, Vertex):
            raise ValueError("val должен быть обьектом Vertex")
        self._v1 = val

    @property
    def v2(self):
        return self._v2

    @v2.setter
    def v2(self, val):
        if not isinstance(val, Vertex):
            raise ValueError("val должен быть обьектом Vertex")
        self._v2 = val

    @property
    def dist(self):
        return self._dist

    @dist.setter
    def dist(self, val):
        if not isinstance(val, int):
            raise ValueError("val должен быть обьектом int")
        self._dist = val

    def __eq__(self, other):
        return hash((self.v1, self.v2)) == hash((other.v1, other.v2)) or hash((self.v1, self.v2)) == hash((other.v2, other.v1))


class Vertex:
    #ID нужен для того чтобы построить матрицу смежности
    __id = -1

    def __new__(cls, *args, **kwargs):
        cls.__id += 1
        return super().__new__(cls)

    def __init__(self):
        self._links = list()
        self._id = self.__id

    @property
    def links(self):
        return self._links

    @links.setter
    def links(self, link: Link):
        if not isinstance(link, Link):
            raise ValueError("Должен быть обьект Link")
        if link not in self._links:
            self._links.append(link)

    @property
    def id(self):
        return self._id

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return hash(self) == hash(other)


class LinkedGraph:
    def __init__(self):
        self._links = list()
        self._vertex = list()

    def __add_vertex(self, vertex):
        if vertex not in self._vertex:
            self._vertex.append(vertex)

    def add_link(self, link):
        if link not in self._links:
            self._links.append(link)
            self.__add_vertex(link.v1)
            self.__add_vertex(link.v2)

    #код с урока
    def find_path(self, start_v, stop_v):
        D = self.__adj_matrix(self._vertex)
        N = len(D)
        Tv = [math.inf]*N
        v = start_v.id
        S = {v}
        Tv[v] = 0  # нулевой вес для стартовой вершины
        M = [0] * N  # оптимальные связи между вершинами
        while v != -1:  # цикл, пока не просмотрим все вершины
            for j, dw in enumerate(D[v]):  # перебираем все связанные вершины с вершиной v
                if j not in S:  # если вершина еще не просмотрена
                    if isinstance(dw, Link):
                        dw = dw.dist
                    w = Tv[v] + dw
                    if w < Tv[j]:
                        Tv[j] = w
                        M[j] = v  # связываем вершину j с вершиной v

            v = self.__arg_min(Tv, S)  # выбираем следующий узел с наименьшим весом
            if v >= 0:  # выбрана очередная вершина
                S.add(v)  # добавляем новую вершину в рассмотрение

        start = start_v.id
        end = stop_v.id
        P = [end]
        while end != start:
            end = M[P[-1]]
            P.append(end)
        P = [vertex for id_vr in P for vertex in self._vertex if vertex.id == id_vr]
        path = P[::-1]
        return path, [link for link in self._links for i in range(len(path)-1) if (link.v1 == path[i] and link.v2 == path[i+1]) or (link.v2 == path[i] and link.v1 == path[i+1])]

    #Метод для построения матрицы смежности
    @staticmethod
    def __adj_matrix(vertexes):
        vertexes.sort(key=lambda x: x.id)
        matrix = []
        for vertex_row in vertexes:
            lst_row = []
            for vertex in vertexes:
                val = 0
                if vertex != vertex_row:
                    val = list(filter(lambda x: (x.v1 == vertex_row and x.v2 == vertex) or (x.v2 == vertex_row and x.v1 == vertex), vertex_row.links))
                    val = val[0] if len(val) == 1 else math.inf
                lst_row.append(val)
            matrix.append(lst_row)
        return matrix

    @staticmethod
    def __arg_min(T, S):
        amin = -1
        m = math.inf  # максимальное значение
        for i, t in enumerate(T):
            if t < m and i not in S:
                m = t
                amin = i

        return amin


class Station(Vertex):
    def __init__(self, name):
        super(Station, self).__init__()
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class LinkMetro(Link):
    pass


#Проверка
map_metro = LinkedGraph()
v1 = Station("Сретенский бульвар")
v2 = Station("Тургеневская")
v3 = Station("Чистые пруды")
v4 = Station("Лубянка")
v5 = Station("Кузнецкий мост")
v6 = Station("Китай-город 1")
v7 = Station("Китай-город 2")

map_metro.add_link(LinkMetro(v1, v2, 1))
map_metro.add_link(LinkMetro(v2, v3, 1))
map_metro.add_link(LinkMetro(v1, v3, 1))

map_metro.add_link(LinkMetro(v4, v5, 1))
map_metro.add_link(LinkMetro(v6, v7, 1))
map_metro.add_link(LinkMetro(v2, v1, 5))
map_metro.add_link(LinkMetro(v2, v7, 5))
map_metro.add_link(LinkMetro(v3, v4, 3))
map_metro.add_link(LinkMetro(v5, v6, 3))

print(len(map_metro._links))
print(len(map_metro._vertex))
path = map_metro.find_path(v1, v6)  # от сретенского бульвара до китай-город 1
print(path[0])    # [Сретенский бульвар, Тургеневская, Китай-город 2, Китай-город 1]
print(sum([x.dist for x in path[1]]))  # 7