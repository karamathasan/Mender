from element import Element2D
from physics.transform import Transform2D
from elements.text import Text
import pygame
import numpy as np
class NodeGraph(Element2D):
    # def __init__(self, *nodes):
        # self.nodes = nodes

    def __init__(self, node_arr, source_target_pairs:np.ndarray):
        """
        Create a Nodal Graph from an order list of nodes and the connections between the source and targets between them
        Args:
            node_arr: the list of N nodes in your graph
            source_target_pairs: a numpy array of shape (2,E). the first row contains the source nodes, and the second row contains the target nodes.
            That is, for the input matrix A, A[0,i] has an edge directed to A[1,i]
        """
    
        self.nodes = node_arr
        # self.nodes = {}
        # for i in range(len(node_arr)):
        #     self.nodes[i] = node_arr[i]
        self.edges = []
        for i in range(len(source_target_pairs[0])):
            source = self.nodes[source_target_pairs[0,i]]
            target = self.nodes[source_target_pairs[1,i]]
            self.edges.append(GraphEdge(source,target))

    def draw(self, camera):
        for edge in self.edges:
            edge.draw(camera)
        for node in self.nodes:
            node.draw(camera)

class GraphEdge():
    def __init__(self, source, target):
        self.source = source
        self.target = target

    def draw(self,camera):
        diff = self.target.transform.position - self.source.transform.position
        dir = diff / np.linalg.norm(diff)
        vecAngle = np.arctan2(dir[1], dir[0]) 

        origin = self.source.transform.position + dir
        end = self.target.transform.position - dir
        pygame.draw.line(camera.screen, "white", origin, end)

        leftDiagonal = np.array([-0.5,0.2])
        rightDiagonal = np.array([-0.5,-0.2])

        leftDiagonal = np.array([
            leftDiagonal[0] * np.cos(vecAngle) - leftDiagonal[1] * np.sin(vecAngle),
            leftDiagonal[0] * np.sin(vecAngle) + leftDiagonal[1] * np.cos(vecAngle)
        ])
        rightDiagonal = np.array([
            rightDiagonal[0] * np.cos(vecAngle) - rightDiagonal[1] * np.sin(vecAngle),
            rightDiagonal[0] * np.sin(vecAngle) + rightDiagonal[1] * np.cos(vecAngle)
        ])
        leftDiagonal += end
        rightDiagonal += end

        origin = camera.Vec2Screen(origin)
        end = camera.Vec2Screen(end)
        pygame.draw.line(camera.screen, "white", origin, end)

        leftDiagonal = camera.Vec2Screen(leftDiagonal)
        rightDiagonal = camera.Vec2Screen(rightDiagonal)
        pygame.draw.polygon(camera.screen, "white", (end, leftDiagonal, rightDiagonal) )

class Node(Element2D):
    def __init__(self, content = None, transform = None, thickness:int = 3):
        self.content = content
        self.transform = transform if transform is not None else Transform2D()
        self.thickness = thickness

    def draw(self, camera):
        origin = camera.Vec2Screen(self.transform.position)
        pygame.draw.circle(camera.screen, "white", origin, camera.toScreenSpace(1), self.thickness)
        #TODO: implement content and text. text should have alphas that allow them to draw over other elements
        # text = Text(str(self.content), np.ndarray(2), self.transform)
        # text.draw(camera)
